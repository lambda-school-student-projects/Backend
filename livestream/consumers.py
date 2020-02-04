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
        print(consumerController)

    def disconnect(self, close_code):
        consumerController.remove(self)

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # print(roomController.toDict())

        for conn in consumerController:
            conn.send(text_data=json.dumps({'message': repr(roomController.toDict())}))


    def chatMessage(self, event):
        message = event['message']

        self.send(text_data=json.dumps({'message': message}))

    # this should actually go somewhere else
    def gameLoop(self):
        alpha = list("abcdefghijklmnopqrstuvwxyz")
        counter = 0
        totalCount = 0
        while True:
            if counter == len(alpha):
                counter = 0
            self.send(text_data=json.dumps({'message':f"{alpha[counter]} {totalCount}"}))
            counter += 1
            totalCount += 1
            print(totalCount)
            time.sleep(1)
