from django.contrib import admin
from .models import Pet, Device, FeedingSchedule, FeedingLog

admin.site.register(Pet)
admin.site.register(Device)
admin.site.register(FeedingSchedule)
admin.site.register(FeedingLog)
