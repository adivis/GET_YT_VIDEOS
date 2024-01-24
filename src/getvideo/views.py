from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage
from django.views.decorators.csrf import csrf_exempt

from getvideo.models import Video
# Create your views here.

@csrf_exempt
def get_videos(request):
    """
    returns the stored video data in a response sorted in descending order of published datetime
    Params - 
    pageNumber = Integer
    """
    
    if request.method != 'GET':
        return JsonResponse({"error":"Method Not Allowed"}, status=405)
    
    # get sorted in descending order ('-' is used as NOT)
    videos = Video.objects.all().order_by('-published_at').values()
    
    # paginator to get number of result on a particular page
    p = Paginator(videos,1)

    # get the page_no from params. If not provided set default to 1
    pageNumber = int(request.GET.get('pageNumber',1))

    try:
        # get the page of specific page number
        page = p.page(pageNumber)
    except EmptyPage:
        return JsonResponse({"error":"Page does not exist"}, status=404)
    
    # find previous page number if exists
    previous_page = page.previous_page_number() if page.has_previous else None
    # find next page number if exists
    next_page = page.next_page_number() if page.has_next else None


    return JsonResponse({
        'videos':list(page),
        'previous_page':previous_page,
        'next_page':next_page
       }, safe=False)