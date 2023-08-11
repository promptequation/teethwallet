import graphene
from appointment.mutations import Mutation as appointment_mutation
from appointment.queries import Query as appointment_query
from auth_extend.mutations import Mutation as auth_mutation
from auth_extend.queries import Query as users
from chat.mutations import Mutation as chat_mutation
from chat.queries import Query as chat_query
from common.mutations import Mutation as common_mutation
from common.queries import Query as common_query
from notification.mutations import Mutation as notification_mutation
from notification.queries import Query as notification_query


class Query(users, common_query, chat_query, appointment_query, notification_query, graphene.ObjectType):
    pass


class Mutation(auth_mutation, common_mutation, chat_mutation, appointment_mutation, notification_mutation,
               graphene.ObjectType):
    pass


schema_api = graphene.Schema(query=Query, mutation=Mutation)
