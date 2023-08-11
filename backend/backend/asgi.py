"""
ASGI config for backend project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os
import django
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()


from channels.auth import AuthMiddlewareStack
from chat.consumers import ChatConsumer
from notification.consumers import RealTimeNotification
from django.urls import re_path,path

websocket_urlpatterns = [
    re_path(r'^ws/chat/(?P<room_name>\w+)/$', ChatConsumer.as_asgi()),
    re_path(r'^ws/notification/(?P<room_name>\w+)/$',RealTimeNotification.as_asgi()),
    
]

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(websocket_urlpatterns)
    ),
})
