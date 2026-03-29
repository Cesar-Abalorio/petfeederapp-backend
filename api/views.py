from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import OrderingFilter
from django.contrib.auth.models import User
from .models import Pet, Device, FeedingSchedule, FeedingLog
from .serializers import UserSerializer, PetSerializer, DeviceSerializer, FeedingScheduleSerializer, FeedingLogSerializer
from api import serializers


# Pagination for React frontend
class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:  # Admin can see all users
            return User.objects.all()
        else:  # Regular users can only see themselves
            return User.objects.filter(id=user.id)
    permission_classes = [IsAuthenticated]
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def me(self, request):
        """Get current authenticated user profile"""
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)


class PetViewSet(viewsets.ModelViewSet):
    serializer_class = PetSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [OrderingFilter]
    ordering_fields = ['name', 'id']
    ordering = ['name']
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Pet.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class DeviceViewSet(viewsets.ModelViewSet):
    serializer_class = DeviceSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [OrderingFilter]
    ordering_fields = ['name', 'status', 'id']
    ordering = ['name']
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Device.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class FeedingScheduleViewSet(viewsets.ModelViewSet):
    serializer_class = FeedingScheduleSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [OrderingFilter]
    ordering_fields = ['time', 'id']
    ordering = ['time']
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return FeedingSchedule.objects.filter(pet__owner=self.request.user)

    def perform_create(self, serializer):
        # Ensure pet and device belong to user
        pet = serializer.validated_data['pet']
        device = serializer.validated_data['device']
        if pet.owner != self.request.user or device.owner != self.request.user:
            raise serializers.ValidationError("Pet and device must belong to the user.")
        serializer.save()


class FeedingLogViewSet(viewsets.ReadOnlyModelViewSet):
    """Read-only logs for monitoring feeding activity"""
    serializer_class = FeedingLogSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [OrderingFilter]
    ordering_fields = ['timestamp', 'id']
    ordering = ['-timestamp']  # Latest first
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return FeedingLog.objects.filter(schedule__pet__owner=self.request.user)


class CustomAuthToken(ObtainAuthToken):
    """Enhanced authentication endpoint for React frontend"""
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        if not serializer.is_valid():
            return Response(
                {'error': 'Invalid username or password'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
        })


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    """Register new user account"""
    username = request.data.get('username')
    password = request.data.get('password')
    email = request.data.get('email')
    
    # Validation
    if not username or not password or not email:
        return Response(
            {'error': 'Username, password, and email are required'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    if len(password) < 6:
        return Response(
            {'error': 'Password must be at least 6 characters'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    if User.objects.filter(username=username).exists():
        return Response(
            {'error': 'Username already exists'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    if User.objects.filter(email=email).exists():
        return Response(
            {'error': 'Email already registered'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Create user
    try:
        user = User.objects.create_user(username=username, password=password, email=email)
        token = Token.objects.create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'username': user.username,
            'email': user.email,
        }, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    """Logout user - delete token"""
    try:
        request.user.auth_token.delete()
        return Response(
            {'message': 'Successfully logged out'},
            status=status.HTTP_200_OK
        )
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def user_profile(request):
    """Get or update current user profile"""
    user = request.user
    if request.method == 'GET':
        serializer = UserSerializer(user)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

