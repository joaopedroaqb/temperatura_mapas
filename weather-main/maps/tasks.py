import time
import requests
from celery import shared_task
from django.conf import settings
from maps.models import WeatherPoint, WeatherPointDetails
import logging
logger = logging.getLogger(__name__)

OPENWEATHER_API_KEY = settings.OPENWEATHER_API_KEY


def fetch_weather_data(url):
    for attempt in range(5):  # Tenta 5 vezes
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 429:
            logger.warning("Limite de requisições atingido. Tentando novamente em 30 segundos.")
            time.sleep(30)  # Espera 30 segundos antes de tentar novamente
        else:
            logger.error(f"Falha ao buscar dados. Código de status: {response.status_code}")
            break
    return None

@shared_task
def update_point_details():
    points = WeatherPoint.objects.all()
    weather_details_to_create = []

    for point in points:
        weather_url = f'https://api.openweathermap.org/data/2.5/weather?lat={point.latitude}&lon={point.longitude}&appid={OPENWEATHER_API_KEY}&units=metric'
        weather_data = fetch_weather_data(weather_url)

        if weather_data:
            weather_details_to_create.append(
                WeatherPointDetails(
                    weather_point=point,
                    climate=weather_data['weather'][0]['description'],
                    humidity=weather_data['main']['humidity'],
                    wind_speed=weather_data['wind']['speed'],
                    precipitation=weather_data.get('rain', {}).get('1h', 0),
                    temperature=weather_data['main']['temp'],
                )
            )
        else:
            logger.error(f"Falha ao recuperar dados para o ponto {point.id} após várias tentativas.")

    if weather_details_to_create:
        WeatherPointDetails.objects.bulk_create(weather_details_to_create)
        logger.info(f"Criados {len(weather_details_to_create)} registros de WeatherPointDetails.")
    else:
        logger.info("Nenhum dado de clima foi atualizado.")