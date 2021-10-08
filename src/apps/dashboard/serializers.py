from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Cards, CardSwapRequestInfo

class CardsSerializers(serializers.ModelSerializer):
    class Meta:
        model = Cards
        fields = '__all__'

class CardSwapRequestInfoSerializers(serializers.ModelSerializer):
    class Meta:
        model = CardSwapRequestInfo
        fields = '__all__'