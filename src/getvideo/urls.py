
from django.urls import path

from getvideo.views import get_videos

urlpatterns = [
    path('', get_videos)
]