import graphene
from api.custom_node import CustomNode
from api.models.user_model import User, UserLang
from django.contrib.auth.models import Group
from graphene_django import DjangoObjectType

from .models import UserSpecialization


class UserType(DjangoObjectType):
    country = graphene.String()

    class Meta:
        model = User
        exclude = ("country",)
        filter_fields = ['id', 'first_name', 'last_name',
                         'email', 'phone', 'gender',
                         'groups', 'street', 'street2']
        interfaces = (CustomNode,)

    def resolve_country(self, info):
        return self.country


class GroupType(DjangoObjectType):
    class Meta:
        model = Group
        filter_fields = ['id', 'name']
        interfaces = (CustomNode,)


class LanguageType(graphene.ObjectType):
    name = graphene.String()
    code = graphene.String()


class NationalityType(graphene.ObjectType):
    name = graphene.String()
    code = graphene.String()


class NationalityType(graphene.ObjectType):
    name = graphene.String()
    code = graphene.String()


class UserSpecializationType(DjangoObjectType):
    class Meta:
        model = UserSpecialization
        fields = "__all__"
        filter_fields = ['id', 'user__id', 'specialization__id']
        interfaces = (CustomNode,)


class UserLangType(DjangoObjectType):
    class Meta:
        model = UserLang
        fields = "__all__"
        filter_fields = ['id', 'user__id', 'lang__id']
        interfaces = (CustomNode,)
