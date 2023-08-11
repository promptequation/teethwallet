import graphene
from graphene_django.filter import DjangoFilterConnectionField
from graphql_jwt.decorators import login_required

from .models import Banned, Connection, Conversation
from .types import BannedType, ConnectionType, ConversationType


class Query(graphene.ObjectType):
    banneds = DjangoFilterConnectionField(BannedType)
    connections = graphene.List(ConnectionType, id=graphene.ID())
    check_connection = graphene.Field(
        ConnectionType, sender=graphene.ID(), receiver=graphene.ID()
    )
    conversations = DjangoFilterConnectionField(
        ConversationType
    )

    @login_required
    def resolve_banneds(self, info, **kwargs):
        return Banned.objects.all()

    @login_required
    def resolve_connections(self, info, id=None, **kwargs):
        if id:
            return Connection.objects.filter(sender__id=id, is_active=True) | Connection.objects.filter(receiver__id=id, is_active=True)
        else:
            return Connection.objects.filter(is_active=True)

    @login_required
    def resolve_check_connection(self, info, sender, receiver):
        connection = Connection.objects.filter(
            sender=sender, receiver=receiver, is_active=True
        ).first()
        if connection:
            return connection
        else:
            return Connection.objects.filter(sender=receiver, receiver=sender, is_active=True).first()

    @login_required
    def resolve_conversations(self, info, **kwargs):
        return Conversation.objects.all()
