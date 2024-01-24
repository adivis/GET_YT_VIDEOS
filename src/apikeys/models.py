from django.db import models

# Create your models here.
class Apikeys(models.Model):
    apikey = models.TextField()
    