from channels.generic.websocket import WebsocketConsumer
import json
import time
from Rooms.RoomModel.RoomController import roomController


consumerController = set()

class RoomConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        for consumer in consumerController:
            consumer.send(text_data=json.dumps({'message': "A new user has connected!!"}))
        consumerController.add(self)
        self.sendIDPrompt()
        # self.gameLoop()

    def disconnect(self, close_code):
        print("close code: ", close_code)
        consumerController.remove(self)

    def receive(self, text_data):
        try:
            text_data_json = json.loads(text_data)
            messageType = text_data_json["messageType"]
            messageData = text_data_json["data"]
        except:
            print("Failed decoding json - booting user.")
            self.close()
        # message = text_data_json['message']

        if messageType == "playerID":
            self.gotPlayerID(messageData)
        elif messageType == "playerPos":
            self.gotPlayerPositionUpdate(messageData)

        # for conn in consumerController: #how to send to all consumers
        #     # conn.send(text_data=json.dumps({'message': "got message"}))
        #     conn.send(text_data=text_data)

    def sendIDPrompt(self):
        self.send(text_data="playerIDReq")

    def gotPlayerID(self, data):
        print(f"got player with id: {data['id']}")

    def gotPlayerPositionUpdate(self, data):
        pass



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
