from django.urls import path
from . import views

app_name = 'observation'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('exposure/', views.StartExposureFormView.as_view(), name='start_exposure'),
]
