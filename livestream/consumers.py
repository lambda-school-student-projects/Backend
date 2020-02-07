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
        # disconnect chat group
        # async_to_sync(self.channel_layer_group_discard)("chat", self.channel_name)
        self.roomController.playerDisconnected(self.player)

    def receive(self, text_data):
        try:
            text_data_json = json.loads(text_data)
            messageType = text_data_json["messageType"]
            messageData = text_data_json["data"]
            # chatData = text_data_json["chat"]
        except:
            print("Failed decoding json - booting user.")
            self.close()
            return

        if messageType == "positionUpdate":
            self.gotPlayerPositionUpdate(messageData)

        # chat send to group
        elif messageType == "chat":
            self.chat_message(messageData)
            
            
            # sefl.chat message(messageData)
            # async_to_sync(self.channel_layer.group_send)(
            #     "chat",
            #     {
            #         "type": "chat.message",
            #         "text": chatData
            #     }
            # )
    
    # chat sending message
    # send message data as param
    def chat_message(self, message):
        # send chat mesg to room => player, mesg
        print(self.player.user.username, message)
        actualMessage = message.get("message", None)
        if actualMessage:
            self.roomController.chatMessageSent(self.player, actualMessage)

        # # send to all players exampe
        # for conn in consumerController: #how to send to all consumers
        #     # conn.send(text_data=json.dumps({'message': "got message"}))
        #     conn.send(text_data=text_data)


    def gotPlayerPositionUpdate(self, data):
        positionList = data["position"]
        position = Position(positionList[0], positionList[1])
        destinationList = data["destination"]
        destination = Position(destinationList[0], destinationList[1])
        self.player.setPosition(position)
        self.player.setDestination(destination)
        # print(self.playerID, id(self.player), position)


    # def chatMessage(self, event):
    #     message = event['message']

    #     self.send(text_data=json.dumps({'message': message}))

    # # this should actually go somewhere else
    # def gameLoop(self):
    #     alpha = list("abcdefghijklmnopqrstuvwxyz")
    #     counter = 0
    #     totalCount = 0
    #     while True:
    #         if counter == len(alpha):
    #             counter = 0
    #         self.send(text_data=json.dumps({'message':f"{alpha[counter]} {totalCount}"}))
    #         counter += 1
    #         totalCount += 1
    #         print(totalCount)
    #         time.sleep(1)
