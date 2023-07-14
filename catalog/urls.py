from django.urls import path

from . import views


app_name = 'catalog'


urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),

    path('content/', views.CatalogItemView.as_view(), name='content'),
    path('graph/visibility/', views.VisibilityChart.as_view(), name='visibility_chart')
]
