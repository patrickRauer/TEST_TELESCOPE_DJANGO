from django.urls import path
from . import views

app_name = 'dome'


urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('auto_aligment/', views.AutoAlignmentFormView.as_view(), name='auto_alignment'),
    path('move/', views.MoveDomeFormView.as_view(), name='move')
]
