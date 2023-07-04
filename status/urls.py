from django.urls import path
from . import views

app_name = 'status'


urlpatterns = [
    path('device/', views.StatusView.as_view(), name='device'),
]
