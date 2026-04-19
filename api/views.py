from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth.models import User
from .serializers import UserSerializer, DeviceSerializer, PetSerializer, FeedingScheduleSerializer, FeedingLogSerializer
from .models import Device, Pet, FeedingSchedule, FeedingLog


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
    """Logout user by deleting their token"""
    try:
        request.user.auth_token.delete()
        return Response({'message': 'Successfully logged out'}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def user_profile(request):
    """Get and update user profile information"""
    if request.method == 'GET':
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def devices(request):
    """List and create devices"""
    if request.method == 'GET':
        devices = Device.objects.filter(owner=request.user)
        serializer = DeviceSerializer(devices, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = DeviceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def scan_devices(request):
    """Scan for available devices"""
    # Placeholder for device scanning logic
    return Response({'message': 'Device scanning not implemented yet'})


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def device_detail(request, device_id):
    """Get, update, or delete a specific device"""
    try:
        device = Device.objects.get(id=device_id, owner=request.user)
    except Device.DoesNotExist:
        return Response({'error': 'Device not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = DeviceSerializer(device)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = DeviceSerializer(device, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        device.delete()
        return Response({'message': 'Device deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def pet_detail(request, pet_id):
    """Get, update, or delete a specific pet"""
    try:
        pet = Pet.objects.get(id=pet_id, owner=request.user)
    except Pet.DoesNotExist:
        return Response({'error': 'Pet not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = PetSerializer(pet)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = PetSerializer(pet, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        pet.delete()
        return Response({'message': 'Pet deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def pets(request):
    """List and create pets"""
    if request.method == 'GET':
        pets = Pet.objects.filter(owner=request.user)
        serializer = PetSerializer(pets, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = PetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def schedule_detail(request, schedule_id):
    """Get, update, or delete a specific feeding schedule"""
    try:
        schedule = FeedingSchedule.objects.get(id=schedule_id, device__owner=request.user)
    except FeedingSchedule.DoesNotExist:
        return Response({'error': 'Schedule not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = FeedingScheduleSerializer(schedule)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = FeedingScheduleSerializer(schedule, data=request.data, context={'request': request}, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        schedule.delete()
        return Response({'message': 'Schedule deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def schedules(request):
    """List and create feeding schedules"""
    if request.method == 'GET':
        user_schedules = FeedingSchedule.objects.filter(device__owner=request.user)
        serializer = FeedingScheduleSerializer(user_schedules, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = FeedingScheduleSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def logs(request):
    """List feeding logs with device information"""
    user_logs = FeedingLog.objects.filter(schedule__device__owner=request.user).select_related('schedule__device')
    serializer = FeedingLogSerializer(user_logs, many=True)
    
    # Enhance the response with device information for frontend compatibility
    enhanced_logs = []
    for log_data in serializer.data:
        log_dict = dict(log_data)
        if log_data.get('schedule'):
            # Get schedule details
            try:
                schedule = FeedingSchedule.objects.select_related('device').get(id=log_data['schedule'])
                log_dict.update({
                    'device_id': schedule.device.id,
                    'device_name': schedule.device.name,
                    'feeding_type': 'Scheduled',
                    'food_level_before': 100,  # Placeholder - would need sensor data
                    'food_level_after': max(0, 100 - schedule.amount),  # Simple calculation
                })
            except FeedingSchedule.DoesNotExist:
                pass
        else:
            # Manual feeding - try to get device from request or use default
            log_dict.update({
                'device_id': 1,  # Default device ID
                'device_name': 'Unknown Device',
                'feeding_type': 'Manual',
                'food_level_before': 100,
                'food_level_after': 50,
            })
        
        enhanced_logs.append(log_dict)
    
    return Response(enhanced_logs)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def feed_device(request):
    """Manually feed a device and create a log entry"""
    device_id = request.data.get('device_id')
    amount = request.data.get('amount', 50)  # Default 50 grams
    schedule_id = request.data.get('schedule_id')  # Optional for scheduled feeds

    if not device_id:
        return Response({'error': 'device_id is required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        device = Device.objects.get(id=device_id, owner=request.user)
        schedule = None
        if schedule_id:
            schedule = FeedingSchedule.objects.get(id=schedule_id, device=device)
        
        log = FeedingLog.objects.create(
            schedule=schedule,
            status='success',
            amount_dispensed=amount
        )
        return Response({
            'message': f'Device {device.name} fed successfully',
            'amount': amount,
            'log_id': log.id
        }, status=status.HTTP_200_OK)
    except Device.DoesNotExist:
        return Response({'error': 'Device not found'}, status=status.HTTP_404_NOT_FOUND)
    except FeedingSchedule.DoesNotExist:
        return Response({'error': 'Schedule not found or does not belong to device'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

