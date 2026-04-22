from django.urls import path
from views import *

urlpatterns = [
    path('temperature/', filter_temp, name='temperature'),
    path('light/', filter_light_status, name='light'),
    path('soil/', filter_soil_moisture, name='soil'),
    path('solution/', fetch_solutions, name='solution'),
    path('disease/', fetch_disease, name='disease'),
]