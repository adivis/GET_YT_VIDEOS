from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from getvideo.models import Video
# Create your views here.

@csrf_exempt
def search_video(request):
    """
    A basic search API to search the stored videos using their title and description.
    """
    
    if request.method != 'GET':
       return JsonResponse({"error":"Method Not Allowed"}, status=405)
   
    # get title and description from params
    title = str(request.GET.get('title',''))
    description = str(request.GET.get('description',''))
    
    #filter out videos containing give title and description    
    allVideos = Video.objects.filter(title__icontains=title).filter(description__icontains=description).values()

    #return filtered videos
    return JsonResponse({
        'video':list(allVideos)
    })