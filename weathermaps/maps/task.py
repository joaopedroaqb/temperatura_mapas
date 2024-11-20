from celery import shared_task
import requests
from .models import FixedPoint, WeatherData

@shared_task
def update_weather_data():
    try:
        # Recupera o ponto fixo
        point = FixedPoint.objects.first()
        if not point:
            return 'Nenhum ponto fixo configurado.'

        api_key = '44f16c65ec07555120f6ad79a49ced74'
        url = f'https://api.openweathermap.org/data/2.5/weather?lat={point.latitude}&lon={point.longitude}&appid={api_key}&units=metric'

        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            WeatherData.objects.create(
                latitude=point.latitude,
                longitude=point.longitude,
                location_name=data.get('name', 'Desconhecida'),
                temperature=data['main']['temp'],
                weather_description=data['weather'][0]['description'],
                humidity=data['main']['humidity'],
                wind_speed=data['wind']['speed'],
            )
            return f'Dados atualizados para o ponto ({point.latitude}, {point.longitude}).'
        else:
            return f'Erro ao buscar dados: {response.status_code}'
    except Exception as e:
        return f'Erro: {e}'


# celery -A weathermaps flower --port=5555                 COMANDO PARA EXECUTAR PRIMEIRO O CELERY
# entrar pela porta http://127.0.0.1:5555 e não a http://0.0.0.0:5555