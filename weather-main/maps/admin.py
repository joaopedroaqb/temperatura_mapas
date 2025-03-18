from django.contrib import admin
from .models import WeatherPoint, WeatherPointDetails

class WeatherPointDetailsInline(admin.TabularInline):
    model = WeatherPointDetails
    extra = 1  # Número de formulários em branco a ser exibido

class WeatherPointAdmin(admin.ModelAdmin):
    list_display = ('name', 'latitude', 'longitude', 'city', 'last_updated')
    search_fields = ('name', 'city')
    list_filter = ('city', 'last_updated')
    inlines = [WeatherPointDetailsInline]

class WeatherPointDetailsAdmin(admin.ModelAdmin):
    list_display = ('weather_point', 'climate', 'humidity', 'wind_speed', 'precipitation', 'temperature', 'created_at')
    list_filter = ('weather_point', 'climate', 'created_at')
    search_fields = ('weather_point__name', 'climate')

admin.site.register(WeatherPoint, WeatherPointAdmin)
admin.site.register(WeatherPointDetails, WeatherPointDetailsAdmin)

#python manage.py createsuperuser
