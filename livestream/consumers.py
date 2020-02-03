from asgiref.sync import async_to_sync
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
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f"data_{self.scope['url_route']['kwargs']['room_name']}"

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()
        # self.gameLoop()


    def disconnect(self, close_code):
        print("disconnected")

        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        print("received something")
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chatMessage',
                'message': message
            }
        )

        # self.send(text_data=json.dumps({'message': message}))
        # self.send(text_data=json.dumps({'message': message}))
        # for test in vars(self.scope):
        #     self.send(text_data=json.dumps({'message': test}))

    def chatMessage(self, event):
        message = event['message']

        self.send(text_data=json.dumps({'message': message}))

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
