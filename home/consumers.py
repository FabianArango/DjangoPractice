import json, random
from asgiref.sync import async_to_sync, sync_to_async
from channels.db import database_sync_to_async
from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
from django.utils import timezone
from . import models

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        print(self.scope['url_route'])
        self.room_name = self.scope['url_route']['kwargs']['AppRoomName']
        print(self.room_name)

        self.room_group_name = 'chat_%s' % self.room_name
        print(self.room_group_name)

        self.room_name += str(random.randrange(0, 10))

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        print(self.scope["cookies"]["username"])

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        print("disconect")
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        print("receive")
        text_data_json = json.loads(text_data)
        message = text_data_json['message']+"(send from ChatConsumer)"+self.room_name

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'message',
                'message': message
            }
        )

    # Receive message from room group
    def message(self, event):
        print("chat_message")
        message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message
        }))


class AsyncChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['AppRoomName']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))   


class UserChat(WebsocketConsumer):
    def connect(self):
        self.chatId = self.scope["url_route"]["kwargs"]["chatId"]
        self.user = models.User.objects.filter(username=self.scope["cookies"]["username"])
        #print(self.chatId)
        if self.user.exists():
            if self.user.get().password == self.scope["cookies"]["password"]:
                print("All si correct")
                self.user = self.user.get()
                self.chat = models.Chat.objects.filter(chatId=self.chatId).get()
                async_to_sync(self.channel_layer.group_add)(
                    self.chatId,
                    self.channel_name
                )

                self.accept()                

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.chatId,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        print(text_data)
        text_data_json = json.loads(text_data)

        message = models.Message(
            content=text_data_json['message'],
            creationDate=timezone.now()
        )
        message.save()
        message.user.add(self.user)
        message.save()
        self.chat.messages.add(message)
        self.chat.save()
        
        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.chatId,
            {   
                'type': 'chat_message',
                "data": [
                    UserChat.buildMessajeJSON(self.user.username, self.user.profilePic.url, message.content)
                ] 
            }
        )

    # Receive message from room group
    def chat_message(self, event):
        self.send(
            text_data=json.dumps(
                event
            )
        )

    @staticmethod
    def buildMessajeJSON(username, profilePic, message):
        return {
            "username": username,
            "profilePic": profilePic,
            "message": message
        }


class RoomServer(WebsocketConsumer):
    def connect(self):
        self.room = self.scope['url_route']['kwargs']['room']
        self.username = self.scope["cookies"]["username"]
        self.color = self.scope["cookies"]["color"]
        self.position = [0, 0]
        self.vel = 6.5

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        inputData = json.loads(text_data)

        if inputData["right"]:
            self.position[0] += self.vel
        
        if inputData["left"]:
            self.position[0] -= self.vel

        if inputData["up"]:
            self.position[1] -= self.vel

        if inputData["down"]:
            self.position[1] += self.vel
        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room,
            {
                'type': 'roomResponse',
                'data': {
                    "username": self.username,
                    "color": self.color,
                    "position": self.position
                }
            }
        )

    def roomResponse(self, data):
        self.send(text_data=json.dumps(data["data"]))

    # Receive message from room group
    def chat_message(self, event):
        #message = event['message']
        print(event["data"])
        # Send message to WebSocket
        self.send(
            text_data=json.dumps(
                event["data"]
            )
        )