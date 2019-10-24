
from django.conf.urls import re_path
from .consumer import ChatConsumer
from .views import ChatManager
from utils.interface_manager import InterfaceManager

Interfaces = {}

websocket_urlpatterns = [
    re_path('chat/', ChatConsumer),
]