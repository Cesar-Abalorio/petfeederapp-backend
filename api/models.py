from django.db import models
from django.contrib.auth.models import User

class Pet(models.Model):
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    breed = models.CharField(max_length=100, blank=True)
    age = models.IntegerField(blank=True, null=True)
    weight = models.FloatField(blank=True, null=True)

    def __str__(self):
        return self.name

class Device(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=[('active', 'Active'), ('inactive', 'Inactive')], default='active')
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class FeedingSchedule(models.Model):
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE)
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    time = models.TimeField()
    amount = models.FloatField()  # grams
    recurring = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.pet.name} at {self.time}"

class FeedingLog(models.Model):
    schedule = models.ForeignKey(FeedingSchedule, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[('success', 'Success'), ('failed', 'Failed')], default='success')
    amount_dispensed = models.FloatField()

    def __str__(self):
        return f"{self.schedule} - {self.timestamp}"
