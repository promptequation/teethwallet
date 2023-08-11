from api.custom_node import CustomNode
from graphene_django import DjangoObjectType

from .models import Banned, Connection, Conversation


class BannedType(DjangoObjectType):
    class Meta:
        model = Banned
        fields = "__all__"
        filter_fields = [
            'source__id', 'destination__id',
            'created_by__id', 'updated_by__id'
        ]
        interfaces = (CustomNode,)


class ConnectionType(DjangoObjectType):
    class Meta:
        model = Connection
        fields = "__all__"
        filter_fields = ['sender', 'receiver', 'created_by', 'updated_by']
        interfaces = (CustomNode,)


class ConversationType(DjangoObjectType):
    class Meta:
        model = Conversation
        fields = "__all__"
        filter_fields = [
            'connection__id', 'sender__id', 'receiver__id',
            'datetime', 'created_by__id', 'updated_by__id'
        ]
        interfaces = (CustomNode,)
