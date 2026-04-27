from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView

urlpatterns = [
    path('auth/', views.CustomAuthToken.as_view(), name='login'),
    path('auth/logout/', views.logout, name='logout'),
    path('register/', views.register, name='register'),
    path('profile/', views.user_profile, name='profile'),
    path('devices/', views.devices, name='devices'), 
    path('devices/<int:device_id>/', views.device_detail, name='device_detail'),
    path('devices/scan/', views.scan_devices, name='scan_devices'),
    path('devices/feed/', views.feed_device, name='feed_device'),
    path('pets/', views.pets, name='pets'),
    path('pets/<int:pet_id>/', views.pet_detail, name='pet_detail'),
    path('schedules/', views.schedules, name='schedules'),
    path('schedules/<int:schedule_id>/', views.schedule_detail, name='schedule_detail'),
    path('logs/', views.logs, name='logs'),
    path('feeding-logs/', views.logs, name='feeding_logs'),  # Alias for frontend compatibility
        path('api/token/', TokenObtainPairView.as_view()) #actived the api/tokenx
]
