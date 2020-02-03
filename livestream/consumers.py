from channels.generic.websocket import WebsocketConsumer
import json
import time


class RoomConsumer(WebsocketConsumer):
    def __init__(self, secondConsumerParameter):
        super().__init__(secondConsumerParameter)
        print("")
        print("NEW consumer started up!")

    def connect(self):
        print("New connection")
        self.accept()
        # self.gameLoop()

    def disconnect(self, close_code):
        print("disconnected")
        pass

    def receive(self, text_data):
        print("received something")
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        self.send(text_data=json.dumps({'message': message}))
        self.send(text_data=json.dumps({'message': message}))
        self.send(text_data=json.dumps({'message': message}))


    def gameLoop(self):
        alpha = list("abcdefghijklmnopqrstuvexyz")
        counter = 0
        totalCount = 0
        while True:
            if counter == len(alpha):
                counter = 0
            self.send(text_data=json.dumps({'message':f"{alpha[counter]} {totalCount}"}))
            counter += 1
            totalCount += 1
            print(totalCount)
            time.sleep(0.05)
