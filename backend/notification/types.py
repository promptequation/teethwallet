from api.custom_node import CustomNode
from graphene_django import DjangoObjectType
from fcm_django.models import FCMDevice
from .models import Notification


class NotificationType(DjangoObjectType):
    class Meta:
        model = Notification
        fields = "__all__"
        filter_fields = ["created_by__id", "created_for__id",
                         "company__id", "notification_type"]
        interfaces = (CustomNode,)


class FCMDeviceObjectType(DjangoObjectType):
    class Meta:
        model = FCMDevice
        fields = "__all__"
        interfaces = (CustomNode,)
