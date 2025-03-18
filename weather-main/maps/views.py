from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import WeatherPoint, WeatherPointDetails
import requests

OPENWEATHER_API_KEY = '44f16c65ec07555120f6ad79a49ced74'


def update_weather_data():
    """
    Atualiza os dados climáticos de todos os pontos registrados no banco de dados.
    """
    points = WeatherPoint.objects.all()
    for point in points:
        weather_url = f'https://api.openweathermap.org/data/2.5/weather?lat={point.latitude}&lon={point.longitude}&appid={OPENWEATHER_API_KEY}&units=metric'
        response = requests.get(weather_url)
        if response.status_code == 200:
            weather_data = response.json()
            point.climate = weather_data['weather'][0]['description']
            point.humidity = weather_data['main']['humidity']
            point.wind_speed = weather_data['wind']['speed']
            point.precipitation = weather_data.get('rain', {}).get('1h', 0)
            point.temperature = weather_data['main']['temp']
            point.save()


def register_point(request):
    """
    Registra um novo ponto com dados de latitude, longitude e nome opcional.
    Busca automaticamente os dados climáticos da API OpenWeather para o ponto.
    """
    if request.method == 'POST':
        lat = request.POST.get('latitude')
        lng = request.POST.get('longitude')
        name = request.POST.get('name')
        if lat and lng:
            weather_url = f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lng}&appid={OPENWEATHER_API_KEY}&units=metric'
            response = requests.get(weather_url)
            if response.status_code == 200:
                weather_data = response.json()
                WeatherPoint.objects.create(
                    name=name or 'Ponto Sem Nome',
                    latitude=lat,
                    longitude=lng,
                    city=weather_data.get('name', 'Desconhecido'),
                )
                return redirect('list_points')
    return render(request, 'maps/register_point.html')


def list_points(request):
    """
    Lista todos os pontos registrados no banco de dados.
    """
    update_weather_data()
    points = list(WeatherPoint.objects.all().values(
        'id', 'latitude', 'longitude', 'name', 'city'
    ))
    return render(request, 'maps/list_points.html', {'points': points})


def point_details(request, point_id):
    """
    Exibe os detalhes de um ponto específico com dados climáticos atualizados.
    """
    point = get_object_or_404(WeatherPoint, id=point_id)
    point_details = WeatherPointDetails.objects.filter(weather_point=point)

    point_data = {
        'id': point.id,
        'name': point.name,
        'latitude': float(point.latitude),
        'longitude': float(point.longitude),
        'city': point.city,
        'details': point_details
    }
    return render(request, 'maps/point_details.html', {'point': point_data})


def api_weather_details(request, point_id):
    """
    Retorna os dados climáticos atualizados de um ponto específico em formato JSON.
    """
    point = get_object_or_404(WeatherPoint, id=point_id)
    # weather_url = f'https://api.openweathermap.org/data/2.5/weather?lat={point.latitude}&lon={point.longitude}&appid={OPENWEATHER_API_KEY}&units=metric'
    # response = requests.get(weather_url)
    point_details = WeatherPointDetails.objects.filter(weather_point=point)

    return JsonResponse({
        'id': point.id,
        'name': point.name,
        'latitude': point.latitude,
        'longitude': point.longitude,
        'city': point.city,
        'point_details': list(point_details.values('climate', 'humidity', 'wind_speed', 'precipitation', 'temperature', 'created_at')),

        'last_updated': point.last_updated.isoformat(),  
    })
