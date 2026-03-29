from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Pet, Device, FeedingSchedule, FeedingLog


class UserSerializer(serializers.ModelSerializer):
    """User data serializer - excludes sensitive info"""
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        read_only_fields = ['id']


class PetSerializer(serializers.ModelSerializer):
    """Pet data with owner info"""
    owner = UserSerializer(read_only=True)

    class Meta:
        model = Pet
        fields = ['id', 'name', 'breed', 'age', 'weight', 'owner']
        read_only_fields = ['id', 'owner']
    
    def validate_name(self, value):
        """Validate pet name"""
        if not value or not value.strip():
            raise serializers.ValidationError("Pet name cannot be empty")
        if len(value) > 100:
            raise serializers.ValidationError("Pet name cannot exceed 100 characters")
        return value


class DeviceSerializer(serializers.ModelSerializer):
    """Device data with owner info"""
    owner = UserSerializer(read_only=True)
    
    class Meta:
        model = Device
        fields = ['id', 'name', 'location', 'status', 'owner']
        read_only_fields = ['id', 'owner']
    
    def validate_name(self, value):
        """Validate device name"""
        if not value or not value.strip():
            raise serializers.ValidationError("Device name cannot be empty")
        return value
    
    def validate_status(self, value):
        """Validate device status"""
        valid_statuses = ['active', 'inactive']
        if value not in valid_statuses:
            raise serializers.ValidationError(f"Status must be one of {valid_statuses}")
        return value


class FeedingScheduleSerializer(serializers.ModelSerializer):
    """Feeding schedule with related pet and device details"""
    pet = serializers.PrimaryKeyRelatedField(queryset=Pet.objects.all())
    device = serializers.PrimaryKeyRelatedField(queryset=Device.objects.all())
    pet_detail = serializers.SerializerMethodField()
    device_detail = serializers.SerializerMethodField()

    class Meta:
        model = FeedingSchedule
        fields = ['id', 'pet', 'pet_detail', 'device', 'device_detail', 'time', 'amount', 'recurring']
        read_only_fields = ['id']

    def get_pet_detail(self, obj):
        """Include pet details in response"""
        return PetSerializer(obj.pet).data
    
    def get_device_detail(self, obj):
        """Include device details in response"""
        return DeviceSerializer(obj.device).data
    
    def validate_amount(self, value):
        """Validate feeding amount"""
        if value <= 0:
            raise serializers.ValidationError("Feeding amount must be greater than 0")
        if value > 1000:
            raise serializers.ValidationError("Feeding amount cannot exceed 1000 grams")
        return value


class FeedingLogSerializer(serializers.ModelSerializer):
    """Feeding activity logs with schedule details"""
    schedule = FeedingScheduleSerializer(read_only=True)
    
    class Meta:
        model = FeedingLog
        fields = ['id', 'schedule', 'timestamp', 'status', 'amount_dispensed']
        read_only_fields = ['id', 'schedule', 'timestamp']
