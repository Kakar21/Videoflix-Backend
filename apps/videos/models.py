from django.db import models
from datetime import date
from apps.users.models import UserAccount


class Video(models.Model):
    CATEGORY_CHOICES = [
        ('documentary', 'Documentary'),
        ('drama', 'Drama'),
        ('romance', 'Romance'),
    ]
        
    created_at = models.DateField(default=date.today)
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=500)
    video_file = models.FileField(upload_to='videos', blank=True, null=True)
    thumbnail = models.ImageField(upload_to='thumbnails', blank=False, null=True)
    category = models.CharField(max_length=16, choices=CATEGORY_CHOICES, default='new')
    new = models.BooleanField(default=True)

    def __str__(self):
        return self.title
    
    
class VideoProgress(models.Model):
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    started = models.BooleanField(default=False)
    last_position = models.FloatField()
    completed = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.email} - {self.video.title} - {self.last_position}"