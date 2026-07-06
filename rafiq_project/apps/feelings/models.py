from django.db import models
from django.conf import settings
from django.utils import timezone


class Feeling(models.Model):
    class EmotionChoices(models.TextChoices):
        Happy = 'happy', 'Happy'
        SAD = 'sad', 'Sad'
        TIRED = 'tired', 'Tired'
        SCARED = 'scared', 'Scared'
        SURPRISE = 'surprise', 'Surprise'
        LOVE = 'love', 'Love'
        ANGRY = 'angry', 'Angry'
        NERVOUS = 'nervous', 'Nervous'
        SHY = 'shy', 'Shy'
        EXCITED = 'excited', 'Excited'
        BORED = 'bored', 'Bored'
        SILLY = 'silly', 'Silly'
        WORRIED = 'worried', 'Worried'
        SICK = 'sick', 'Sick'

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='feelings')
    emotion = models.CharField(max_length=16, choices=EmotionChoices.choices)
    reason = models.TextField(blank=True)
    created_at = models.DateTimeField(default=timezone.now, db_index=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user} - {self.emotion} @ {self.created_at.isoformat()}"
