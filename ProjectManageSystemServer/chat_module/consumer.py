
from django.conf import settings
from channels.generic.websocket import AsyncWebsocketConsumer
from enum import Enum
import json, random, datetime

class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):

        self.joined_groups = {}

        self.close_connection = False

        self.ip_address = self.scope['client']
