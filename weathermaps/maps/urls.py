from django.urls import path
from . import views

urlpatterns = [
    # Página principal com o mapa meteorológico
    path('', views.weather_map, name='weather_map'),

    # Endpoint para salvar o ponto selecionado
    path('save-point/', views.save_point, name='save_point'),

    # Página para exibir os dados meteorológicos armazenados
    path('dashboard/', views.weather_dashboard, name='weather_dashboard'),
]
