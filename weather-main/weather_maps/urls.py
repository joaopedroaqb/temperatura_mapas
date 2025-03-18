from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', lambda request: redirect('list_points')),  # Redireciona a URL raiz para a lista de pontos
    path('', include('maps.urls')),  # Inclui as URLs do app "maps"
]
