import os.path
from django.http import JsonResponse
import json

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from django.conf import settings
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt 
def get_videos(request):
    if request.method != 'GET':
        return JsonResponse({"error":"Method Not Allowed"}, status=405)

    service = build('youtube', 'v3', developerKey=settings.API_SECRET_KEY)
    try:
        api_response = service.search().list(part="snippet",q="makeup", maxResults=1).execute()

        
        return JsonResponse({"message":api_response['items']}, status=200)
        for item in api_response['items']:
            print(item['snippet'])
        

    except HttpError as e:
        print("Yes")
        print(e)