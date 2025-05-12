from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class LoginDevice(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='forum_logindevice')
    user_agent = models.TextField()
    ip_address = models.GenericIPAddressField()
    login_time = models.DateTimeField(auto_now_add=True)

    def parsed_agent(self):
        return self.user_agent[:100]  

    def __str__(self):
        return f"{self.user.username} - {self.ip_address} @ {self.login_time}"

class Category(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Topic(models.Model):
    title = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    views = models.PositiveIntegerField(default=0)
    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    @property
    def latest_post_by(self):
        last_post = self.posts.order_by('-created_at').first()
        return last_post.created_by.username if last_post else "Nog geen posts"

class Post(models.Model):
    topic = models.ForeignKey(Topic, related_name='posts', on_delete=models.CASCADE)
    content = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Post by {self.created_by.username} on {self.created_at}"
        
class ChatMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class VisitorFingerprint(models.Model):
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField()
    path = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.ip_address} - {self.timestamp}"

class FingerprintData(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField()
    screen_resolution = models.CharField(max_length=20)
    language = models.CharField(max_length=50)
    timezone = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.ip_address} - {self.timestamp}"