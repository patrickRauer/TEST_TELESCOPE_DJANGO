from django.urls import path
from . import views

app_name = 'camera'


urlpatterns = [
    path('status/', views.CameraStatusView.as_view(), name='status'),
    path('exposure/', views.TakeImageFormView.as_view(), name='exposure'),
    path('exposure/current/<int:image_id>/', views.CurrentExposureView.as_view(), name='current_exposure')
]
