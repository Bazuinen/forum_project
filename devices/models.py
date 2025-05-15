from django.db import models
from django.contrib.auth.models import User

class LoginDevice(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='login_devices')
    user_agent = models.TextField()
    ip_address = models.GenericIPAddressField()
    login_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.ip_address} @ {self.login_time}"

class VisitorFingerprint(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField()
    path = models.CharField(max_length=255)
    screen_width = models.CharField(max_length=20, blank=True, null=True)
    screen_height = models.CharField(max_length=20, blank=True, null=True)
    language = models.CharField(max_length=50, blank=True, null=True)
    platform = models.CharField(max_length=100, blank=True, null=True)
    timezone = models.CharField(max_length=100, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username if self.user else 'Guest'} - {self.ip_address} - {self.timestamp}"


