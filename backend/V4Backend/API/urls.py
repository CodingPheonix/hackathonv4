from django.contrib import admin
from django.urls import path
from .views import agent, hello

urlpatterns = [
    path('agent/', agent, name='agent'),
    path('hello/', hello, name='hello'),

    # path('test_soil/', test_get_soil_moisture, name="test_get_soil_moisture"),
    # path('test_light/', get_light, name="get_light_index"),
    # path('get_weather_ranges/', get_weather_r, name="get_weather_ranges"),
    # path('extract_from_prompt/', extract_from_prompt, name="extract_from_prompt"),
    # path('fetch_weather/', fetch_weather, name="fetch_weather"),
    # path('compile_weather_status/', compile_weather_status, name="compile_weather_status"),
]