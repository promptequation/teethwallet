from django.urls import re_path
from .consumers import RealTimeNotification


websocket_urlpatterns = [
    re_path(r'^ws/notification/(?P<room_name>\w+)/$',
            RealTimeNotification.as_asgi()),
]
