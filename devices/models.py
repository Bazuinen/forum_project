from django.db import models
from django.contrib.auth.models import User

class LoginDevice(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_agent = models.TextField()
    ip_address = models.GenericIPAddressField()
    login_time = models.DateTimeField(auto_now_add=True)

    def parsed_agent(self):
        # Simpele parsing (kan ook met 'httpagentparser' of 'user-agents' package)
        return self.user_agent[:100]  # of iets als: return parse(self.user_agent)

    def __str__(self):
        return f"{self.user.username} - {self.ip_address} @ {self.login_time}"

class Category(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class VisitorFingerprint(models.Model):
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField()
    path = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.ip_address} - {self.timestamp}"

class FingerprintData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='devices_fingerprintdata')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='devices_logindevice')
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField()
    screen_resolution = models.CharField(max_length=20)
    language = models.CharField(max_length=50)
    timezone = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.ip_address} - {self.timestamp}"