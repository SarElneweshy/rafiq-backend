from django.db import models
from django.conf import settings
from django.utils import timezone

class JournalEntry(models.Model):
    JOURNAL_TYPE_CHOICES = (
        ('text', 'Text'),
        ('voice', 'Voice'),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    journal_type = models.CharField(max_length=10, choices=JOURNAL_TYPE_CHOICES)
    content_text = models.TextField(blank=True, null=True)
    content_voice = models.FileField(upload_to='journal_voices/%Y/%m/%d/', blank=True, null=True)
    detected_language = models.CharField(max_length=10, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
         return f"{self.journal_type} - {self.user.username} - {self.created_at.date()}"
    