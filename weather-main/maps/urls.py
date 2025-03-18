from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_point, name='register_point'),
    path('points/', views.list_points, name='list_points'),
    path('points/<int:point_id>/', views.point_details, name='point_details'),
    path('api/weather/<int:point_id>/', views.api_weather_details, name='api_weather_details'),  # Nova rota
]
