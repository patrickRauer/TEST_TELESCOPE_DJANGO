from django.urls import path
from . import views


app_name = 'mount'


urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('slew/', views.SlewFormView.as_view(), name='slew'),
    path('park/', views.ParkFormView.as_view(), name='park'),
    path('status/', views.StatusView.as_view(), name='status'),
]