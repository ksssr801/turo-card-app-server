from rest_framework import routers, urlpatterns
from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import RegisterApi

# router = DefaultRouter()
urlpatterns = [
    path('register', RegisterApi.as_view())
]
