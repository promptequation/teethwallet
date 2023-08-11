import graphene
from django.db.models import Q
from .models import Notification
from .types import NotificationType


class Query(graphene.ObjectType):
    notifications = graphene.List(NotificationType, user_id=graphene.Int())

    def resolve_notifications(self, info, user_id=None):
        if user_id:
            return Notification.objects.filter(Q(created_for=user_id))
        else:
            return Notification.objects.all()
