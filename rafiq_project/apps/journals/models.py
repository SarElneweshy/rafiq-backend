from django.db import models
from django.conf import settings

class Journal(models.Model):
     user = models.ForeignKey( settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='journals')
     content = models.TextField()
     language = models.CharField(max_length=5, default='en')
     emotions = models.JSONField()
     dominant_emotion = models.CharField(max_length=20, default='neutral')
     created_at = models.DateTimeField(auto_now_add=True)
     updated_at = models.DateTimeField(auto_now=True)

    
     def __str__(self):
        return f"{self.user.username} - {self.dominant_emotion}"