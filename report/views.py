from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.conf import settings
import os

def image_view(request, filename):
    image_path = os.path.join(settings.MEDIA_ROOT, 'images', filename)
    with open(image_path, 'rb') as f:
        image_data = f.read()
    return HttpResponse(image_data, content_type='image/jpeg')
def home_view(request):
    return render(request, 'home.html')
