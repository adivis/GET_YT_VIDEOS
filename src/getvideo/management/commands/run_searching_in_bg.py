import sys
from time import sleep
import datetime
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
    count = 0
    for video in videos['items']:
        if 'videoId' in video['id']:
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
                count += 1
    return count

def search_video(query, max_res, next_page):
    """search videos with the given parameters"""

    service = build(API_NAME, API_VERSION, developerKey=API_SECRET_KEY)

    try:
        api_response = service.search().list(part="snippet",q=query, maxResults=max_res, pageToken=next_page).execute()
        return api_response
    
    # If quota is exceeded
    except HttpError as e:
        raise e

class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        self.stdout.write("Started the search...")
        sys.stdout.flush()

        next_page = None
        new_video_add_db = 0
        tot_video_add = 0
        while True:
            try:
                videos = search_video("keys",50, next_page)
                number_of_vid = len(videos['items'])
                if number_of_vid >0:
                    new_video_add_db = save_video(videos)
                    tot_video_add += new_video_add_db
                    
                #check if there is a next page in the response
                #if yes then set it as page token
                #else come out of the loop
                if number_of_vid>0 and 'nextPageToken' in videos:
                    next_page = videos['nextPageToken']
                else:
                    break
                message = 'At ' + str(datetime.datetime.now()) +'\nadded '+str(new_video_add_db)+' new videos in db. Total videos added '+str(tot_video_add)
                self.stdout.write(message)
                
            except HttpError as e:
                raise (e)
            finally:
                sys.stdout.flush()
                sleep(int(API_TIME_INTERVAL))


