from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth.models import User
from .serializers import UserSerializer


class CustomAuthToken(ObtainAuthToken):
    """Authentication endpoint for frontend"""
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        if not serializer.is_valid():
            return Response({'error': 'Invalid username or password'}, status=status.HTTP_401_UNAUTHORIZED)

        user = serializer.validated_data['user']
        token, _ = Token.objects.get_or_create(user=user)

        return Response({'token': token.key, 'user_id': user.pk, 'username': user.username, 'email': user.email, 'first_name': user.first_name, 'last_name': user.last_name})


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    """Register new user account"""
    username = request.data.get('username')
    password = request.data.get('password')
    email = request.data.get('email')

    if not username or not password or not email:
        return Response({'error': 'Username, password, and email are required'}, status=status.HTTP_400_BAD_REQUEST)

    if len(password) < 6:
        return Response({'error': 'Password must be at least 6 characters'}, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(username=username).exists():
        return Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(email=email).exists():
        return Response({'error': 'Email already registered'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = User.objects.create_user(username=username, password=password, email=email)
        token = Token.objects.create(user=user)
        return Response({'token': token.key, 'user_id': user.pk, 'username': user.username, 'email': user.email}, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    """Logout user by deleting token"""
    try:
        request.user.auth_token.delete()
        return Response({'message': 'Successfully logged out'}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def user_profile(request):
    """Get or update current user profile"""
    if request.method == 'GET':
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
    
    serializer = UserSerializer(request.user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 

from .models import Device
from .serializers import DeviceSerializer

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def devices(request):
    if request.method == 'GET':
        user_devices = Device.objects.filter(user=request.user)
        serializer = DeviceSerializer(user_devices, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        data = request.data.copy()
        data['user'] = request.user.id

        serializer = DeviceSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=400)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def pets(request):
    from .models import Pet
    from rest_framework import serializers

    class PetSerializer(serializers.ModelSerializer):
        class Meta:
            model = Pet
            fields = "__all__"

    if request.method == 'GET':
        user_pets = Pet.objects.filter(owner=request.user)
        serializer = PetSerializer(user_pets, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        data = request.data.copy()
        data['owner'] = request.user.id

        serializer = PetSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=400)
  