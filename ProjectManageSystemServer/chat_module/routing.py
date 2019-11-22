
from django.conf.urls import re_path
from .consumer import ChatConsumer
from .views import ChatView
from utils.interface_manager import InterfaceManager

Interfaces = {}

websocket_urlpatterns = [
    re_path('chat/', ChatConsumer),
]