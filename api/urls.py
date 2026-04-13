from django.urls import path
from . import views

urlpatterns = [
    path('auth/', views.CustomAuthToken.as_view(), name='login'),
    path('auth/logout/', views.logout, name='logout'),
    path('register/', views.register, name='register'),
    path('profile/', views.user_profile, name='profile'),
    path('devices/', views.devices, name='devices'), 
    path('devices/scan/', views.scan_devices, name='scan_devices'),
    path('devices/feed/', views.feed_device, name='feed_device'),
    path('pets/', views.pets, name='pets'),
    path('schedules/', views.schedules, name='schedules'),
    path('logs/', views.logs, name='logs'),
]
