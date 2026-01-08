from django.db import models

class Doctor(models.Model):
  
    name = models.CharField(max_length=255)
    specialty = models.CharField(max_length=255)
    language = models.CharField(max_length=100, blank=True, null=True)
   
    rating = models.FloatField(default=0)
    reviews_count = models.IntegerField(default=0)
    
    joined_months_ago = models.IntegerField(default=0)
    sessions_count = models.IntegerField(default=0)
    
    price_60_min = models.IntegerField()
    price_30_min = models.IntegerField()

    image = models.URLField(blank=True, null=True)
   
    certificates = models.JSONField(default=list, blank=True)

    available_days = models.JSONField(default=list, blank=True)  
    
    def __str__(self):
        return self.name
