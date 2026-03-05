from django.contrib import admin
from django.urls import path
from .views import agent, hello

urlpatterns = [
    path('agent/', agent, name='agent'),
    path('hello/', hello, name='hello'),
]