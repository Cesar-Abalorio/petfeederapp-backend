from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Device, Pet, FeedingSchedule, FeedingLog


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        read_only_fields = ['id']


class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = "__all__"


class PetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pet
        fields = "__all__"
        read_only_fields = ['owner']


class FeedingScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeedingSchedule
        fields = "__all__"


class FeedingLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeedingLog
        fields = "__all__"
    