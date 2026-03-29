from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'users', views.UserViewSet, basename='user')
router.register(r'pets', views.PetViewSet, basename='pet')
router.register(r'devices', views.DeviceViewSet, basename='device')
router.register(r'schedules', views.FeedingScheduleViewSet, basename='schedule')
router.register(r'logs', views.FeedingLogViewSet, basename='log')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', views.CustomAuthToken.as_view()),
]