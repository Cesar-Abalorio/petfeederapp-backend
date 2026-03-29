from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import Pet, Device, FeedingSchedule, FeedingLog
from .serializers import UserSerializer, PetSerializer, DeviceSerializer, FeedingScheduleSerializer, FeedingLogSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class PetViewSet(viewsets.ModelViewSet):
    serializer_class = PetSerializer

    def get_queryset(self):
        return Pet.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class DeviceViewSet(viewsets.ModelViewSet):
    serializer_class = DeviceSerializer

    def get_queryset(self):
        return Device.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class FeedingScheduleViewSet(viewsets.ModelViewSet):
    serializer_class = FeedingScheduleSerializer

    def get_queryset(self):
        return FeedingSchedule.objects.filter(pet__owner=self.request.user)

    def perform_create(self, serializer):
        # Ensure pet and device belong to user
        pet = serializer.validated_data['pet']
        device = serializer.validated_data['device']
        if pet.owner != self.request.user or device.owner != self.request.user:
            raise serializers.ValidationError("Pet and device must belong to the user.")
        serializer.save()

class FeedingLogViewSet(viewsets.ReadOnlyModelViewSet):  # Read-only for logs
    serializer_class = FeedingLogSerializer

    def get_queryset(self):
        return FeedingLog.objects.filter(schedule__pet__owner=self.request.user)

class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })
