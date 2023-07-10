import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer


class ObservationConsumer(WebsocketConsumer):
    observation_id = None

    def connect(self):
        print('new connection')
        self.observation_id = f'obs_{self.scope["url_route"]["kwargs"]["obs_id"]}'
        async_to_sync(
            self.channel_layer.group_add
        )(
            self.observation_id, self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.observation_id, self.channel_name
        )

    def receive(self, text_data):
        print(self.__dict__)
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        self.send(text_data=json.dumps({"message": message}))

    def observation_update(self, event):
        print(event)
        self.send(
            text_data=event['text']
        )
