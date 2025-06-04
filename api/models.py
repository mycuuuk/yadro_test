from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import string
import random

def generate_short_code(length=6):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choices(characters, k=length))

class Link(models.Model):
    original_url = models.URLField()
    short_code = models.CharField(max_length=10, unique=True, default=generate_short_code)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    click_count = models.PositiveIntegerField(default=0)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def is_expired(self):
        return timezone.now() > self.expires_at

    def __str__(self):
        return f"{self.short_code} -> {self.original_url}"

class ClickLog(models.Model):
    link = models.ForeignKey(Link, on_delete=models.CASCADE, related_name='click_logs')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Click at {self.timestamp} for {self.link.short_code}"