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
        fields = ['id', 'name', 'location', 'status', 'ip_address', 'mac_address', 'owner']
        read_only_fields = ['owner']


class PetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pet
        fields = "__all__"
        read_only_fields = ['owner']


class FeedingScheduleSerializer(serializers.ModelSerializer):
    pet = serializers.PrimaryKeyRelatedField(queryset=Pet.objects.all())
    device = serializers.PrimaryKeyRelatedField(queryset=Device.objects.all())
    pet_id = serializers.IntegerField(write_only=True, required=False)
    device_id = serializers.IntegerField(write_only=True, required=False)
    time = serializers.TimeField(input_formats=['%H:%M', '%H:%M:%S'])

    class Meta:
        model = FeedingSchedule
        fields = ['id', 'pet', 'device', 'time', 'amount', 'recurring', 'pet_id', 'device_id']

    def to_internal_value(self, data):
        data = data.copy()
        if 'pet_id' in data and 'pet' not in data:
            data['pet'] = data.pop('pet_id')
        if 'device_id' in data and 'device' not in data:
            data['device'] = data.pop('device_id')
        return super().to_internal_value(data)

    def validate(self, attrs):
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            user = request.user
            device = attrs.get('device')
            pet = attrs.get('pet')
            if device and device.owner != user:
                raise serializers.ValidationError({'device': 'Device does not belong to the authenticated user.'})
            if pet and pet.owner != user:
                raise serializers.ValidationError({'pet': 'Pet does not belong to the authenticated user.'})
        return attrs


class FeedingLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeedingLog
        fields = "__all__"
        extra_kwargs = {
            'schedule': {'allow_null': True}
        }
    