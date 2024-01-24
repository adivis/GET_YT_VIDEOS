from django.http import JsonResponse

from getvideo.models import Video
# Create your views here.


def get_videos(request):
    """returns the stored video data in a response sorted in descending order of published datetime """
    if request.method != 'GET':
        return JsonResponse({"error":"Method Not Allowed"}, status=405)
    
    # get sorted in descending order ('-' is used as NOT)
    videos = Video.objects.all().order_by('-published_at').values()

    return JsonResponse(list(videos), safe=False)