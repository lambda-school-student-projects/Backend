from channels.generic.websocket import WebsocketConsumer
import json


class RoomConsumer(WebsocketConsumer):
    def connect(self):
        print("New connection")
        self.accept()

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


    