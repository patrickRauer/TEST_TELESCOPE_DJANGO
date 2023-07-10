from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path("ws/observation/running/<str:obs_id>/", consumers.ObservationConsumer.as_asgi()),
]
