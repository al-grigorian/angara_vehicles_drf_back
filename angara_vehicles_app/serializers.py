from .models import *
from rest_framework import serializers
 
 
class ComponentSerializer(serializers.ModelSerializer):
    class Meta:
        # Модель, которую мы сериализуем
        model = Components
        # Поля, которые мы сериализуем
        fields = "__all__"
 
class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        # Модель, которую мы сериализуем
        model = Applications
        # Поля, которые мы сериализуем
        fields = "__all__"
 
class ApplicationComponentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicationsComponents
        fields = '__all__'