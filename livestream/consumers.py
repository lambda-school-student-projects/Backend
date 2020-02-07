from channels.generic.websocket import WebsocketConsumer
import json
import time
from Rooms.bsvPosition import Position
from Rooms.models import Player
from asgiref.sync import async_to_sync

consumerController = {}

class RoomConsumer(WebsocketConsumer):

    def __init__(self, secondArg):
        super().__init__(secondArg)
        from Rooms.bsvRoomController import roomController
        self.roomController = roomController

    def connect(self):
        self.accept()
        try:
            self.playerID = self.scope['url_route']['kwargs']['playerID']
        except:
            print("No user idea provided - booting user.")
            self.send(text_data="Need user id")
            self.close()
            return
        consumerController[self.playerID] = self
        self.player = self.roomController.allPlayers[self.playerID]

    def disconnect(self, close_code):
        print("close code: ", close_code)
        consumerController.pop(self.playerID, None)
        self.roomController.playerDisconnected(self.player)

    def receive(self, text_data):
        try:
            text_data_json = json.loads(text_data)
            messageType = text_data_json["messageType"]
            messageData = text_data_json["data"]
        except:
            print("Failed decoding json - booting user.")
            self.close()
            return

        if messageType == "positionUpdate":
            self.gotPlayerPositionUpdate(messageData)

        # chat send to group
        elif messageType == "chat":
            self.chat_message(messageData)

    
    # chat sending message
    # send message data as param
    def chat_message(self, message):
        # send chat mesg to room => player, mesg
        print(self.player.user.username, message)
        actualMessage = message.get("message", None)
        if actualMessage:
            self.roomController.chatMessageSent(self.player, actualMessage)



    def gotPlayerPositionUpdate(self, data):
        positionList = data["position"]
        position = Position(positionList[0], positionList[1])
        destinationList = data["destination"]
        destination = Position(destinationList[0], destinationList[1])
        self.player.setPosition(position)
        self.player.setDestination(destination)
        # print(self.playerID, id(self.player), position)
