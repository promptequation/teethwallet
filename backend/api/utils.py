import graphene
import graphql_jwt
from api.models.user_model import User
from auth_extend.types import UserType
from graphql import GraphQLError
import datetime
from dateutil.relativedelta import relativedelta
import pytz

utc = pytz.UTC


class ObtainJSONWebToken(graphql_jwt.JSONWebTokenMutation):
    user = graphene.Field(UserType)

    @classmethod
    def resolve(cls, root, info, **kwargs):
        return cls(user=info.context.user)


class CustomObtainJSONWebToken(ObtainJSONWebToken):
    message = graphene.String()

    @classmethod
    def mutate(cls, *args, **kwargs):
        user = User.objects.filter(username=kwargs['username']).first()
        if user:
            user = User.objects.get(username=kwargs['username'])
            if user:
                if user.is_active == True:
                    if user.counter == 0:
                        user.counter = 1
                        user.save()
                        return super().mutate(*args, **kwargs)
                    else:
                        end_date = utc.localize(datetime.datetime.now())
                        if user.is_first_login == True or user.end_login_date == None or user.end_login_date > end_date:
                            user.is_first_login = False
                            user.save()
                        else:
                            user.is_first_login = True
                            user.counter = 0
                            user.end_login_date = datetime.datetime.now() + relativedelta(months=6)
                            user.save()
                        return super().mutate(*args, **kwargs)

                if user.is_active == False:
                    raise GraphQLError(
                        'Your Email is not verified. Please verify your email.')
            else:
                raise Exception("Please enter valid credentials.")
        else:
            raise Exception("Please enter valid credentials.")
