from django.db import models

class Doctor(models.Model):
    name = models.CharField(max_length=200)
    sub_specialty = models.CharField(max_length=500, blank=True)
    city = models.CharField(max_length=100,db_index=True)
    area = models.CharField(max_length=100, blank=True, db_index=True)
    address = models.CharField(max_length=500, blank=True)
    rating = models.FloatField(null=True, blank=True)
    reviews_count = models.IntegerField(default=0)
    price = models.IntegerField(null=True, blank=True)
    image_url = models.URLField(blank=True)
    vezeeta_url = models.URLField(unique=True)
    is_active = models.BooleanField(default=True)
    scraped_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering =['-rating', '-reviews_count']

        verbose_name         = 'Doctor'
        verbose_name_plural  = 'Doctors'

    def __str__(self):
        return f"{self.name} — {self.city}"


class ScrapingLog(models.Model):
    STATUS_CHOICES = [
        ('success', 'Success'),
        ('failed', 'Failed'),
        ('partial', 'Partial'),
    ]
    started_at = models.DateTimeField(auto_now_add=True)
    finished_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES,default='partial')
    city = models.CharField(max_length=100)
    saved = models.IntegerField(default=0)
    updated = models.IntegerField(default=0)
    deactivated = models.IntegerField(default=0)
    error = models.TextField(blank=True)

    class Meta:
        ordering = ['-started_at']

    def __str__(self):
        return f"{self.city} | {self.status} | {self.started_at:%Y-%m-%d %H:%M}"
