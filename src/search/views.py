from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from getvideo.models import Video
# Create your views here.

@csrf_exempt
def search_video(request):
    """
    A basic search API to search the stored videos using their title and description.
    Params - 
    title="tea how"
    description="something over"
    """
    
    if request.method != 'GET':
       return JsonResponse({"error":"Method Not Allowed"}, status=405)
   
    # get title and description from params
    title = str(request.GET.get('title',''))
    description = str(request.GET.get('description',''))
    
    # get separate words in title and description
    title = title.split(' ')
    description = description.split(' ')
    
    allVideos = Video.objects.all()
    # allVideos = Video.objects.filter(title__icontains=title[0]).filter(description__icontains=description)
    
    # check all the words of title separately
    for word in title:
        allVideos = allVideos.filter(title__icontains=word)
        
    # check all the words of description separately
    for word in description:
        allVideos = allVideos.filter(description__icontains=word)
        
    #filter out videos containing give title and description    
    
    #return filtered videos
    return JsonResponse({
        'video':list(allVideos.values())
    })