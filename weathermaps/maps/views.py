from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import json
from .models import FixedPoint, WeatherData


def weather_map(request):
    """
    Exibe a página do mapa meteorológico.
    """
    context = {
        'layers': [
            'clouds_new',
            'precipitation_new',
            'pressure_new',
            'wind_new',
            'temp_new',
        ],
        'api_key': settings.OPENWEATHER_API_KEY,  # Certifique-se de ter essa variável no settings.py
    }
    return render(request, 'maps/weather_map.html', context)


@csrf_exempt
def save_point(request):
    """
    Salva o ponto selecionado no mapa no banco de dados.
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            lat = data['lat']
            lng = data['lng']

            # Salva ou atualiza o ponto fixo
            FixedPoint.objects.update_or_create(
                id=1,  # Usa sempre o mesmo ID para garantir um único ponto salvo
                defaults={'latitude': lat, 'longitude': lng}
            )
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)
    return JsonResponse({'success': False, 'error': 'Método inválido'}, status=405)


def weather_dashboard(request):
    """
    Exibe os dados climáticos armazenados no banco de dados.
    """
    data = WeatherData.objects.all().order_by('-timestamp')[:10]  # Últimos 10 registros
    return render(request, 'maps/weather_dashboard.html', {'data': data})
