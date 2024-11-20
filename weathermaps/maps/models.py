from django.db import models

class WeatherData(models.Model):
    """
    Armazena dados meteorológicos coletados de um ponto fixo.
    """
    latitude = models.FloatField()  # Latitude do local onde os dados foram coletados
    longitude = models.FloatField()  # Longitude do local onde os dados foram coletados
    location_name = models.CharField(max_length=100)  # Nome da localização (se disponível)
    temperature = models.FloatField()  # Temperatura em graus Celsius
    weather_description = models.CharField(max_length=255)  # Descrição do clima (ex.: "nublado", "ensolarado")
    humidity = models.FloatField()  # Umidade relativa (%)
    wind_speed = models.FloatField()  # Velocidade do vento (m/s)
    timestamp = models.DateTimeField(auto_now_add=True)  # Data e hora da coleta dos dados

    def __str__(self):
        return f'{self.location_name} ({self.latitude}, {self.longitude})'


class FixedPoint(models.Model):
    """
    Armazena o ponto fixo selecionado pelo usuário no mapa.
    """
    latitude = models.FloatField()  # Latitude do ponto fixo
    longitude = models.FloatField()  # Longitude do ponto fixo
    timestamp = models.DateTimeField(auto_now=True)  # Última vez que o ponto foi atualizado

    def __str__(self):
        return f'Ponto Fixo ({self.latitude}, {self.longitude})'
