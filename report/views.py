import os

from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render, redirect

from API import models

def home_view(request):

    return render(request, 'home.html')


from django.shortcuts import render, redirect



def image_view(request, filename):
    image_path = os.path.join(settings.MEDIA_ROOT, 'images', filename)
    with open(image_path, 'rb') as f:
        image_data = f.read()
    return HttpResponse(image_data, content_type='image/jpeg')