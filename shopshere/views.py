from django.http import HttpResponse

def home(request):
    return HttpResponse('My Homepage and this is old')