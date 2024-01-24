from django.contrib.admin import ModelAdmin
from django.contrib import admin
from getvideo.models import Video
# Register your models here.

class VideoAdmin(ModelAdmin):
    
    list_display = ('videoId','title','published_at')
    search_fields = ('videoId','title','description')
    ordering = ['published_at']
    list_filter = ['published_at']
    
admin.site.register(Video, VideoAdmin)

    