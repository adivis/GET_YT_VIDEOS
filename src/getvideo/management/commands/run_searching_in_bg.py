import sys
from time import sleep
import datetime
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from django.core.management.base import BaseCommand
from django.conf import settings

from getvideo.models import Video
from apikeys.models import Apikeys

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
                    publishedAt = video['snippet']['publishedAt'],
                    thumbnailUrls = {
                        'default': video['snippet']['thumbnails']['default']['url'],
                        'medium': video['snippet']['thumbnails']['medium']['url'],
                        'high': video['snippet']['thumbnails']['high']['url'],
                    }
                )
                count += 1
    return count

def search_video(query, max_res, next_page, API_SECRET_KEY):
    """search videos with the given parameters"""

    service = build(API_NAME, API_VERSION, developerKey=API_SECRET_KEY)

    try:
        api_response = service.search().list(part="snippet",q=query, maxResults=max_res, pageToken=next_page, order="date").execute()
        return api_response
    
    # If quota is exceeded
    except HttpError as e:
        raise e

class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        self.stdout.write("Started the search...")
        sys.stdout.flush()

        apikeys = Apikeys.objects.all()      
        active_api_key = apikeys.first().apikey if apikeys.exists() else "something"
        query = "official"

        next_page = None
        new_video_add_db = 0
        tot_video_add = 0
        api_key_idx = 0
        
        while True:
            try:
                videos = search_video(query,50, next_page,active_api_key)
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
                display_message = 'At ' + str(datetime.datetime.now()) +'\nadded '+str(new_video_add_db)+' new videos in db. Total videos added '+str(tot_video_add)
                self.stdout.write(display_message)
                
            except HttpError as e:    
                # error if no apikey exists in db
                if not apikeys.exists():
                    self.stdout.write("No apiket exists in DB. Add some.")
                    break
                
                #  Core API errors
                if e.resp['status'] == '400':
                    self.stdout.write(e.reason)
                    break
                    
                if e.resp['status'] == '403':
                    self.stdout.write('Either access is forbidden or quota exceeded. Moving on to the next api key.')
                    api_key_idx = api_key_idx + 1
                    if api_key_idx >= apikeys.count():
                        self.stdout.write('No next key present. Add more keys.')
                        break
                    active_api_key = apikeys[api_key_idx].apikey
                    
                # any other error
                else:
                    self.stderr.write(e)
                
            finally:
                sys.stdout.flush()
                sleep(int(API_TIME_INTERVAL)/1000)


