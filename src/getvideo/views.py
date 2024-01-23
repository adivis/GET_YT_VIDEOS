from django.http import JsonResponse

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

API_SECRET_KEY = settings.API_SECRET_KEY
API_VERSION = 'v3'
API_NAME = 'youtube'
@csrf_exempt 
def get_videos(request):
    if request.method != 'GET':
        return JsonResponse({"error":"Method Not Allowed"}, status=405)

    service = build(API_NAME, API_VERSION, developerKey=API_SECRET_KEY)
    try:
        api_response = service.search().list(part="snippet",q="makeup", maxResults=1).execute()

        
        for item in api_response['items']:
            print(item['snippet'])
        return JsonResponse({"message":api_response['items']}, status=200)
        

    except HttpError as e:
        print("Yes")
        print(e)