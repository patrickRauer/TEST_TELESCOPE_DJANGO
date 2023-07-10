from django.urls import path
from . import views

app_name = 'camera'


urlpatterns = [
    path('', views.CameraIndexView.as_view(), name='index'),
    path('status/', views.CameraStatusView.as_view(), name='status'),
    path('temperature/graph/', views.CameraTemperatureView.as_view(), name='temperature_graph'),
    path('exposure/', views.TakeImageFormView.as_view(), name='exposure'),
    path('exposure/current/<int:image_id>/', views.CurrentExposureView.as_view(), name='current_exposure')
]
