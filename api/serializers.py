from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Pet, Device, FeedingSchedule, FeedingLog

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

class PetSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)

    class Meta:
        model = Pet
        fields = '__all__'

class DeviceSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)

    class Meta:
        model = Device
        fields = '__all__'

class FeedingScheduleSerializer(serializers.ModelSerializer):
    pet = serializers.PrimaryKeyRelatedField(queryset=Pet.objects.all())
    device = serializers.PrimaryKeyRelatedField(queryset=Device.objects.all())

    class Meta:
        model = FeedingSchedule
        fields = '__all__'

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['pet'] = PetSerializer(instance.pet).data
        rep['device'] = DeviceSerializer(instance.device).data
        return rep

class FeedingLogSerializer(serializers.ModelSerializer):
    schedule = FeedingScheduleSerializer(read_only=True)

    class Meta:
        model = FeedingLog
        fields = '__all__'