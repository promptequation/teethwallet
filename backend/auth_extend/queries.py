import graphene
from api.enums.nationality_enum import NationalityEnum
from api.models.user_model import User, UserLang
from api.utils import ObtainJSONWebToken
from django.contrib.auth.models import Group
from django_countries import countries
from django_countries.graphql.types import Country
from graphene_django.filter import DjangoFilterConnectionField
from graphql_jwt.decorators import login_required
from backend import settings
from .models import UserSpecialization
from .types import UserSpecializationType, UserLangType
from .types import UserType, GroupType, LanguageType, NationalityType


class Query(graphene.ObjectType):
    viewer = graphene.Field(UserType, token=graphene.String(required=True))
    token_auth = ObtainJSONWebToken.Field()
    country_list = graphene.List(Country)
    language_list = graphene.List(LanguageType)
    nationality_list = graphene.List(NationalityType)
    users = DjangoFilterConnectionField(UserType, input=graphene.String())
    user = graphene.Field(UserType, user_id=graphene.Int())
    groups = graphene.List(GroupType)

    @login_required
    def resolve_viewer(self, info, **kwargs):
        return info.context.user

    @login_required
    def resolve_users(self, info, input=None, **kwargs):
        if input:
            return User.objects.filter(groups__name=input)
        else:
            return User.objects.all()

    @login_required
    def resolve_user(self, info, user_id: int):
        return User.objects.get(id=user_id)

    @login_required
    def resolve_groups(self, info, **kwargs):
        return Group.objects.all()

    def resolve_country_list(self, info, **kwargs):
        return list(countries)

    def resolve_language_list(self, info, **kwargs):
        return [LanguageType(code=_len[0], name=_len[1]) for _len in settings.LANGUAGES]

    def resolve_nationality_list(self, info, **kwargs):
        return [NationalityType(code=_ne.value, name=_ne.name) for _ne in NationalityEnum]

    userSpecializations = DjangoFilterConnectionField(
        UserSpecializationType, user_id=graphene.ID())

    @login_required
    def resolve_userSpecializations(self, info, user_id=None, **kwargs):
        if user_id:
            return UserSpecialization.objects.filter(user__id=user_id)

    userLang = graphene.List(UserLangType, user_id=graphene.ID())

    @login_required
    def resolve_userLang(self, info, user_id=None, **kwargs):
        if user_id:
            return UserLang.objects.filter(user__id=user_id)
