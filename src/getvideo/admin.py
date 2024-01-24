from django.contrib.admin import ModelAdmin
from django.contrib import admin
from getvideo.models import Video


class VideoAdmin(ModelAdmin):
    list_display = ('videoId', 'title', 'publishedAt')
    search_fields = ('videoId', 'title', 'description')
    ordering = ['publishedAt']
    list_filter = ['publishedAt']


admin.site.register(Video, VideoAdmin)
