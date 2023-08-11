import graphene
from api.models.user_model import User
from django.db.models import Q

from .models import Banned, Connection, Conversation
from .types import BannedType, ConnectionType, ConversationType


class BannedInput(graphene.InputObjectType):
    id = graphene.ID()
    source = graphene.Int()
    destination = graphene.Int()
    remarks = graphene.String()
    is_deleted = graphene.Boolean()
    created_by = graphene.Int()
    updated_by = graphene.Int()


class CreateBanned(graphene.Mutation):
    """ Example:
        mutation {
          createBanned(bannedData: {
          source: 1,
          destination: 1,
          remarks: "test remarks",
          isDeleted: false,
          createdBy: 1,
          updatedBy: 1}) {
            banned {
              id
            }
          }
        }
    """

    class Arguments:
        banned_data = BannedInput()

    banned = graphene.Field(BannedType)

    @staticmethod
    def mutate(root, info, banned_data=None):
        banned_instance = Banned(
            source=banned_data.source,
            destination=banned_data.destination,
            remarks=banned_data.remarks,
            is_deleted=banned_data.is_deleted,
            created_by_id=banned_data.created_by or banned_data.source,
            updated_by_id=banned_data.updated_by or banned_data.source,
        )
        banned_instance.save()
        return CreateBanned(banned=banned_instance)


class UpdateBanned(graphene.Mutation):
    """
    Example:
        mutation {
          updateBanned(bannedData:
          {
          id: 1,
          remarks:
          "test remarks updated",
          isDeleted: false,
          updatedBy: 1
          })
          {
            banned {
              id
              remarks
              sourceId {
                username
              }
            }
          }
        }


    """

    class Arguments:
        banned_data = BannedInput(required=True)

    banned = graphene.Field(BannedType)

    @staticmethod
    def mutate(root, info, banned_data=None):
        banned_instance = Banned.objects.get(pk=banned_data.id)

        if banned_instance:
            banned_instance.remarks = banned_data.remarks
            banned_instance.updated_by_id = banned_data.updated_by
            banned_instance.is_deleted = banned_data.is_deleted or False
            banned_instance.save()

            return UpdateBanned(banned=banned_instance)
        return UpdateBanned(banned=None)


class DeleteBanned(graphene.Mutation):
    """
    Example:
        mutation {
          deleteBanned(id: 1) {
            banned {
              source {
                username
                id
              }
            }
          }
        }
    """

    class Arguments:
        id = graphene.ID()

    banned = graphene.Field(BannedType)

    @staticmethod
    def mutate(root, info, id):
        banned_instance = Banned.objects.get(pk=id)
        banned_instance.delete()
        return None


class ConnectionInput(graphene.InputObjectType):
    sender = graphene.ID()
    receiver = graphene.ID()
    created_by = graphene.ID()
    updated_by = graphene.ID()


class CreateConnection(graphene.Mutation):
    """
    Example:
       mutation {
  createConnection(connectionData: {sender: 1, receiver: 1, createdBy: 1, updatedBy: 1}) {
    connection {
      id
      sender {
        id
        username
      }
    }
  }
}

    """

    class Arguments:
        input = ConnectionInput()

    connection = graphene.Field(ConnectionType)

    @staticmethod
    def mutate(root, info, input=None):
        sender = User.objects.get(pk=input.sender)
        receiver = User.objects.get(pk=input.receiver)

        try:
            criterion1 = Q(sender=input.sender)
            criterion2 = Q(receiver=input.receiver)

            criterion3 = Q(sender=input.receiver)
            criterion4 = Q(receiver=input.sender)

            connection_count = Connection.objects.filter(
                (criterion1 & criterion2) | (criterion3 & criterion4)).count()

            if connection_count > 0:
                connection = Connection.objects.filter(
                    (criterion1 & criterion2) | (criterion3 & criterion4))
                connection_instance = connection.first()
                return CreateConnection(connection=connection_instance)
            elif connection_count == 0:
                connection_instance = Connection(
                    sender=sender,
                    receiver=receiver,
                    created_by=input.created_by or sender,
                    updated_by=input.updated_by or sender,
                )
                connection_instance.save()
                return CreateConnection(connection=connection_instance)

        except:
            connection_instance = Connection(
                sender=sender,
                receiver=receiver,
                created_by=input.created_by or sender,
                updated_by=input.updated_by or sender,
            )
            connection_instance.save()
            return CreateConnection(connection=connection_instance)


class UpdateConnection(graphene.Mutation):
    """
    Example:
        mutation {
          updateConnection(connectionData: {id: 1,  updatedBy: 1}) {
            connection {
              id
              sender {
                id
                username
              }
            }
          }
        }
    """

    class Arguments:
        input = ConnectionInput(required=True)

    connection = graphene.Field(ConnectionType)

    @staticmethod
    def mutate(root, info, input=None):
        sender = User.objects.get(pk=input.sender)
        receiver = User.objects.get(pk=input.receiver)
        connection_instance = Connection.objects.get(pk=input.id)

        if connection_instance:
            connection_instance.sender = sender
            connection_instance.receiver = receiver
            connection_instance.updated_by = input.updated_by or sender
            connection_instance.created_by = input.created_by or sender
            connection_instance.save()

            return UpdateConnection(connection=connection_instance)
        return UpdateConnection(connection=None)


class DeleteConnection(graphene.Mutation):
    """
    Example:
        mutation{
          deleteConnection(id:1){
            connection{
              sender{
                username,
                id
              }
            }
          }
        }
    """

    class Arguments:
        id = graphene.ID()

    connection = graphene.Field(ConnectionType)

    @staticmethod
    def mutate(root, info, id):
        connection_instance = Connection.objects.get(pk=id)
        connection_instance.delete()
        return None


class ConversationInput(graphene.InputObjectType):
    connection = graphene.ID()
    message = graphene.String()
    sender = graphene.ID()
    receiver = graphene.ID()
    is_seen = graphene.Boolean()
    is_edited = graphene.Boolean()
    created_by = graphene.ID()
    updated_by = graphene.ID()
    is_auto_message = graphene.Boolean()


class CreateConversation(graphene.Mutation):
    """
    Examples:
        mutation {
          createMessages(input: {connection: 2, message: "Test Conversation", sender: 1, receiver: 1, isSeen: false, isEdited: false, createdBy: 1, updatedBy: 1}) {
            messages {
              id
              message
              datetime
              sender {
                id
                username
              }
            }
          }
        }
    """

    class Arguments:
        input = ConversationInput()

    conversation = graphene.Field(ConversationType)

    @staticmethod
    def mutate(root, info, input=None):
        sender = User.objects.get(pk=input.sender)
        receiver = User.objects.get(pk=input.receiver)
        connection = Connection.objects.get(pk=input.connection)
        conversation_instance = Conversation(
            connection=connection,
            message=input.message,
            sender=sender,
            receiver=receiver,
            is_seen=input.is_seen or False,
            is_edited=input.is_edited or False,
            is_auto_message = input.is_auto_message or False,
            created_by=input.created_by or sender,
            updated_by=input.updated_by or sender,
        )
        conversation_instance.save()
        return CreateConversation(conversation=conversation_instance)


class UpdateConversation(graphene.Mutation):
    """
    Examples:
        mutation {
          updateMessages(messagesData: {id: 1, messageBody: "updated", isSeen: true, isEdited: true}) {
            messages {
              id
              messageBody
              updatedAt
              updatedBy {
                id
                username
              }
            }
          }
        }
    """

    class Arguments:
        input = ConversationInput()

    conversation = graphene.Field(ConversationType)

    @staticmethod
    def mutate(root, info, input=None):
        conversation_instance = Conversation.objects.get(
            pk=input.id
        )
        if conversation_instance:
            conversation_instance.connection = input.connection or conversation_instance.connection
            conversation_instance.message = input.message
            conversation_instance.is_seen = input.is_seen or False
            conversation_instance.is_edited = input.is_edited or False
            conversation_instance.is_auto_message = input.is_auto_message or False
            conversation_instance.save()

            return UpdateConversation(conversation=conversation_instance)
        return UpdateConversation(conversation=None)


class DeleteConversation(graphene.Mutation):
    """
    Examples:
        mutation {
          deleteMessages(id: 2) {
            messages {
              id
            }
          }
        }
    """

    class Arguments:
        id = graphene.ID()

    conversation = graphene.Field(ConversationType)

    @staticmethod
    def mutate(root, info, id):
        conversation_instance = Conversation.objects.get(pk=id)
        conversation_instance.delete()
        return None


class Mutation(graphene.ObjectType):
    create_banned = CreateBanned.Field()
    update_banned = UpdateBanned.Field()
    delete_banned = DeleteBanned.Field()

    create_connection = CreateConnection.Field()
    update_connection = UpdateConnection.Field()
    delete_connection = DeleteConnection.Field()

    create_conversation = CreateConversation.Field()
    update_conversation = UpdateConversation.Field()
    delete_conversation = DeleteConversation.Field()
