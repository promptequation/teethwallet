import graphene
import graphql_jwt
from api.models import User
from api.tasks import registration_send_email
from api.utils import CustomObtainJSONWebToken
from common.models import Specialization
from django.contrib.auth.models import Group
from django.shortcuts import get_object_or_404
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from .confirmation_email import send_confirmation_email, email_confirmation_text
from .email_verification_token import account_activation_token
from .models import UserSpecialization
from .types import UserSpecializationType
from .types import UserType, GroupType
from api.models.user_model import MultiLanguage
from graphql import GraphQLError


class GroupInput(graphene.InputObjectType):
    name = graphene.String()


class CreateGroup(graphene.Mutation):
    class Arguments:
        input = GroupInput()

    group = graphene.Field(GroupType)

    @staticmethod
    def mutate(root, info, input=None):
        group_instance = Group(name=input.name)
        group_instance.save()
        return CreateGroup(group=group_instance)


class UserInput(graphene.InputObjectType):
    firstName = graphene.String()
    lastName = graphene.String()
    username = graphene.String()
    email = graphene.String()
    password = graphene.String()
    date_of_birth = graphene.Date()
    street = graphene.String()
    street2 = graphene.String()
    country = graphene.String()
    nationality = graphene.Int()
    language_code = graphene.String()
    lang = graphene.ID()
    is_caregiver = graphene.Boolean()


class CreateUser(graphene.Mutation):
    class Arguments:
        input = UserInput()

    user = graphene.Field(UserType)

    @staticmethod
    def mutate(root, info, input=None):
        if User.objects.filter(email=input.email):
            raise GraphQLError('The Email has already been taken.')
        if User.objects.filter(username=input.username):
            raise GraphQLError('The Username has already been taken.')
        try:
            lang = MultiLanguage.objects.get(pk=input.lang)
            user_instance = User(
                first_name=input.firstName,
                last_name=input.lastName,
                email=input.email,
                username=input.username,
                name=str(input.firstName) + ' ' + str(input.lastName),
                street=input.street,
                street2=input.street2,
                country=input.country,
                date_of_birth=input.date_of_birth,
                nationality=input.nationality,
                language_code=input.language_code,
                lang=lang,
                is_caregiver=input.is_caregiver
            )
            user_instance.set_password(input.password)
            user_instance.is_active = False
            user_instance.save()
            send_confirmation_email(email=input.email, user=user_instance)
            user_group = Group.objects.get(name='Patient')
            user_instance.groups.add(user_group)
            return CreateUser(user=user_instance)
        except:
            raise GraphQLError("Please fill all the fields properly")


class UserGroupInput(graphene.InputObjectType):
    id = graphene.ID()
    group = graphene.String()


class UpdateRemoveGroup(graphene.Mutation):
    class Arguments:
        input = UserGroupInput()

    user = graphene.Field(UserType)

    @staticmethod
    def mutate(root, info, input=None):
        usergroup_instance = User.objects.get(pk=input.id)
        group = Group.objects.get(name=input.group)
        user_patient_group = usergroup_instance.groups.filter(
            name='Patient').exists()
        user_doctor_group = usergroup_instance.groups.filter(
            name='Doctor').exists()
        doctor = Group.objects.get(name='Doctor')
        patient = Group.objects.get(name='Patient')
        if group.name == "Doctor":
            if user_patient_group:
                usergroup_instance.groups.remove(patient)
                usergroup_instance.groups.add(doctor)
        if group.name == "Patient":
            if user_doctor_group:
                usergroup_instance.groups.remove(doctor)
                usergroup_instance.groups.add(patient)
        return UpdateRemoveGroup(user=usergroup_instance)


class UserUpdateInput(graphene.InputObjectType):
    id = graphene.ID()
    first_name = graphene.String()
    last_name = graphene.String()
    email = graphene.String()
    username = graphene.String()
    phone = graphene.String()
    gender = graphene.String()
    street = graphene.String()
    street2 = graphene.String()
    city = graphene.String()
    zip = graphene.String()
    country = graphene.String()
    avatar = graphene.String()
    nationality = graphene.Int()
    date_of_birth = graphene.Date()
    language_code = graphene.String()
    lang = graphene.ID()
    is_caregiver = graphene.Boolean()
    access_survey = graphene.Boolean()


class UpdateUser(graphene.Mutation):
    class Arguments:
        input = UserUpdateInput()

    user = graphene.Field(UserType)

    @staticmethod
    def mutate(root, info, input=None):
        user_instance = User.objects.get(pk=input.id)
        multilanguage = MultiLanguage.objects.get(pk=input.lang)
        if user_instance:
            if input.first_name:
                user_instance.first_name = input.first_name
            if input.last_name:
                user_instance.last_name = input.last_name
            if input.email:
                user_instance.email = input.email
            if input.username:
                user_instance.username = input.username
            if input.phone:
                user_instance.phone = input.phone
            if input.date_of_birth:
                user_instance.date_of_birth = input.date_of_birth
            if input.gender:
                user_instance.gender = input.gender
            if input.avatar:
                user_instance.avatar = input.avatar
            if input.street:
                user_instance.street = input.street
            if input.street2 == "":
                user_instance.street2 = ""
            elif input.street2 != "":
                user_instance.street2 = input.street2
            if input.city:
                user_instance.city = input.city
            if input.zip:
                user_instance.zip = input.zip
            if input.country:
                user_instance.country = input.country
            if input.nationality:
                user_instance.nationality = input.nationality
            if input.language_code:
                user_instance.language_code = input.language_code
            if input.lang:
                user_instance.lang = multilanguage
            if input.is_caregiver is not None:
                user_instance.is_caregiver = input.is_caregiver or False
            if input.access_survey is not None:
                user_instance.access_survey = input.access_survey
            user_instance.save()
            return UpdateUser(user=user_instance)
        return UpdateUser(user=None)


class UserSpecializationInput(graphene.InputObjectType):
    user = graphene.ID()
    specialization = graphene.ID()


class CreateUserSpecialization(graphene.Mutation):
    class Arguments:
        input = UserSpecializationInput()

    userspecialization = graphene.Field(UserSpecializationType)

    @staticmethod
    def mutate(root, info, input=None):
        user = get_object_or_404(User, pk=input.user)
        specialization = get_object_or_404(
            Specialization, pk=input.specialization)
        userspecialization_instance = UserSpecialization(
            user=user,
            specialization=specialization,
        )
        userspecialization_instance.save()
        return CreateUserSpecialization(userspecialization=userspecialization_instance)


class DeleteUserSpecialization(graphene.Mutation):
    class Arguments:
        user = graphene.ID()

    delete_specialization = graphene.Field(UserSpecializationType)

    @staticmethod
    def mutate(root, info, user):
        user = get_object_or_404(User, pk=user)
        if user:
            user_specialization = UserSpecialization.objects.filter(user=user)
            user_specialization.delete()
            return None


class SendEmailInvitation(graphene.Mutation):
    class Arguments:
        email = graphene.String()

    response = graphene.String()

    @staticmethod
    def mutate(root, info, email):
        user_instance = User.objects.filter(email=email)
        if (user_instance):
            return SendEmailInvitation(response="This email already have an account.")
        else:
            user_instance.email = email
            registration_send_email(user_instance)
            return SendEmailInvitation(response="Email sent!")


class EmailVerifyInput(graphene.InputObjectType):
    uuid = graphene.String()
    email_token = graphene.String()


class VerifyEmail(graphene.Mutation):
    class Arguments:
        input = EmailVerifyInput()

    user = graphene.Field(UserType)

    @staticmethod
    def mutate(root, info, input=None):
        uuid = force_text(urlsafe_base64_decode(input.uuid))
        user = User.objects.get(pk=uuid)
        if user is not None and account_activation_token.check_token(user, input.email_token):
            user.is_active = True
            user.save()
            email_confirmation_text(user=user)
        return VerifyEmail(user=user)


class ResendVerificationEmail(graphene.Mutation):
    class Arguments:
        email = graphene.String()

    response = graphene.String()
    user = graphene.Field(UserType)

    @staticmethod
    def mutate(root, info, email):
        user_instance = User.objects.get(email=email)
        if user_instance.is_active == False:
            send_confirmation_email(email=email, user=user_instance)
        else:
            return ResendVerificationEmail(
                user=user_instance,
                response="You have already verified your email with us. Thanks!"
            )
        return ResendVerificationEmail(
            user=user_instance,
            response="A verification link has been sent to your email account."
        )


class Mutation(graphene.ObjectType):
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()
    sendEmailInvitation = SendEmailInvitation.Field()
    token_auth = CustomObtainJSONWebToken.Field()
    create_user = CreateUser.Field()
    create_group = CreateGroup.Field()
    update_user = UpdateUser.Field()
    update_user_group = UpdateRemoveGroup.Field()
    create_user_specialization = CreateUserSpecialization.Field()
    delete_user_specialization = DeleteUserSpecialization.Field()
    delete_token_cookie = graphql_jwt.DeleteJSONWebTokenCookie.Field()
    delete_refresh_token_cookie = graphql_jwt.DeleteRefreshTokenCookie.Field()
    email_verification = VerifyEmail.Field()
    resend_verification_email = ResendVerificationEmail.Field()
