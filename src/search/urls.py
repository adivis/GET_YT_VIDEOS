from django.urls import path

from search.views import search_video

urlpatterns = [
    path('', search_video)
]