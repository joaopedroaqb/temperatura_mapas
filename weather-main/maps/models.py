from django.db import models

class WeatherPointDetails(models.Model):
    weather_point = models.ForeignKey('WeatherPoint', on_delete=models.CASCADE)
    climate = models.CharField(max_length=100, blank=True, null=True)
    humidity = models.FloatField(blank=True, null=True)
    wind_speed = models.FloatField(blank=True, null=True)
    precipitation = models.FloatField(blank=True, null=True)
    temperature = models.FloatField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.weather_point.name

class WeatherPoint(models.Model):
    name = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()
    city = models.CharField(max_length=100, blank=True, null=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name