import sys
from time import sleep

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from django.core.management.base import BaseCommand
from django.conf import settings

from getvideo.models import Video

API_SECRET_KEY = settings.API_SECRET_KEY
API_VERSION = 'v3'
API_NAME = 'youtube'
API_TIME_INTERVAL = settings.API_TIME_INTERVAL

def save_video(videos):
    """save video that are not saved in db"""

    for video in videos['items']:
        if not Video.objects.filter(videoId=video['id']['videoId']):
            Video.objects.create(
                videoId=video['id']['videoId'],
                title = video['snippet']['title'],
                description = video['snippet']['description'],
                published_at = video['snippet']['publishedAt'],
                thumbnail_urls = {
                    'default': video['snippet']['thumbnails']['default']['url'],
                    'medium': video['snippet']['thumbnails']['medium']['url'],
                    'high': video['snippet']['thumbnails']['high']['url'],
                }
            )

def search_video(query, maxResults):
    """search videos with the given parameters"""

    service = build(API_NAME, API_VERSION, developerKey=API_SECRET_KEY)

    try:
        api_response = service.search().list(part="snippet",q=query, maxResults=maxResults).execute()
        return api_response
    
    except HttpError as e:
        print("Yes")
        print(e)

class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        self.stdout.write("Started the search...")
        sys.stdout.flush()

        while True:
            try:
                videos = search_video("keys",1)
                save_video(videos)
                
            except HttpError as e:
                print(e)
            finally:
                sys.stdout.flush()
                sleep(int(API_TIME_INTERVAL))


