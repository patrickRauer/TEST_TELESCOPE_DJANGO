from django.urls import path
from . import views

app_name = 'observation'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('exposure/', views.StartExposureFormView.as_view(), name='start_exposure'),
    path('running/<int:obs_id>/', views.OngoingExposureView.as_view(), name='running_exposure'),
    path('running/<int:image_id>/image', views.ImageView.as_view(), name='image'),
]
