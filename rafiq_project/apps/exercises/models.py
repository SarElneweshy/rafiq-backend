from django.db import models

class Disorder(models.Model):
    short_name = models.CharField(max_length=50)  # ADHD – MDD – PTSD
    full_name = models.CharField(max_length=255)  # Attention-Deficit/Hyperactivity Disorder

    class Meta:
        
        ordering = ['id']

    def __str__(self):
        return self.short_name
    
class Exercise(models.Model):
    disorder = models.ForeignKey(
        Disorder, on_delete=models.CASCADE, related_name='exercises')
    title = models.CharField(max_length=255)
    short_desc = models.TextField()
    detailed_desc = models.TextField()

    video_url = models.URLField(null=True, blank=True)

    class Meta:
       
        ordering = ['id']

    def __str__(self):
        return f"{self.disorder.short_name} - {self.title}"
