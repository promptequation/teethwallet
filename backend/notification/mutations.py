import graphene
from api.models.user_model import User
from common.models import Company
from common.handle_error import get_object_or_None
from fcm_django.models import FCMDevice
from .models import Notification
from .types import NotificationType, FCMDeviceObjectType


class NotificationInput(graphene.InputObjectType):
    id = graphene.ID()
    is_read = graphene.Boolean()


class NotificationCreate(graphene.Mutation):
    class Arguments:
        input = NotificationInput()

    notification = graphene.Field(NotificationType)

    @staticmethod
    def mutate(root, info, input=None):
        notification_instance = Notification(
            created_by=User.objects.get(id=input.user),
            created_for=User.objects.get(id=input.user),
            company=Company.objects.get(id=input.user),
            notification_type=input.notification_type,
            notification_message=input.notification_message
        )
        notification_instance.save()
        return NotificationCreate(notification=notification_instance)


class DeleteNotification(graphene.Mutation):
    class Arguments:
        input = graphene.ID()

    notification = graphene.Field(NotificationType)

    @staticmethod
    def mutate(root, info, input):
        notification_instance = get_object_or_None(Notification, pk=input)
        notification_instance.delete()
        return None


class UpdateNotification(graphene.Mutation):
    class Arguments:
        input = NotificationInput()

    notification = graphene.Field(NotificationType)

    @staticmethod
    def mutate(root, info, input=None):
        notification_instance = get_object_or_None(Notification, pk=input.id)
        if notification_instance:
            notification_instance.is_read = input.is_read
            notification_instance.save()
            return UpdateNotification(notification=notification_instance)
        return None


class FCMdeviceInput(graphene.InputObjectType):
    name = graphene.String()
    user = graphene.ID()
    registration_id = graphene.String()
    type = graphene.String()
    device_id = graphene.String()
    active = graphene.Boolean()


class CreateFCMDevice(graphene.Mutation):
    class Arguments:
        input = FCMdeviceInput()

    fcm_device = graphene.Field(FCMDeviceObjectType)

    @staticmethod
    def mutate(root, info, input=None):
        try:
            if FCMDevice.objects.get(device_id=input.device_id, user_id=input.user):
                fcm_device_instance = FCMDevice.objects.get(
                    device_id=input.device_id, user_id=input.user)
                fcm_device_instance.name = input.name
                fcm_device_instance.registration_id = input.registration_id
                fcm_device_instance.active = input.active
                fcm_device_instance.type = input.type
                fcm_device_instance.save()
                return CreateFCMDevice(fcm_device=fcm_device_instance)
        except:
            fcm_device_instance, created = FCMDevice.objects.update_or_create(
                name=input.name,
                user=User.objects.get(id=input.user),
                registration_id=input.registration_id,
                type=input.type,
                device_id=input.device_id,
                active=input.active
            )
            return CreateFCMDevice(fcm_device=fcm_device_instance)


class Mutation(graphene.ObjectType):
    create_notification = NotificationCreate.Field()
    delete_notification = DeleteNotification.Field()
    update_notification = UpdateNotification.Field()
    create_fcm_device = CreateFCMDevice.Field()
