from django.db import models

# Create your models here.

class Video(models.Model):
    title = models.TextField()  # Youtube video title
    description = models.TextField()
    published_at = models.DateTimeField()  # Timestamp of published date and time
    thumbnail_urls = models.JSONField()  # All URL for the thumbnail

    class Meta:
        # Database Indexes 
        
        indexes = [
            models.Index(fields=['published_at']), # for sorting index on published_at
            models.Index(fields=['title']),# for searching
            models.Index(fields=['description']),#for searching
        ]
