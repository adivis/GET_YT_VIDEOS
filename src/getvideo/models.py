from django.db import models

# Create your models here.


class Video(models.Model):
    videoId = models.CharField(max_length=11, unique=True)  # unique id associated with every youtube video
    title = models.TextField()  # Youtube video title
    description = models.TextField()
    publishedAt = models.DateTimeField()  # Timestamp of published date and time
    thumbnailUrls = models.JSONField()  # All URL for the thumbnail

    class Meta:
        # Database Indexes

        indexes = [
            models.Index(fields=['publishedAt']),  # for sorting index on publishedAt
            models.Index(fields=['title']),  # for searching
            models.Index(fields=['description']),  # for searching
            models.Index(fields=['videoId']),  # for searching and filtering
        ]
