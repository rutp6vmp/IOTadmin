from django.contrib import admin
from API.models import *

class ImageDataAdmin(admin.ModelAdmin):
    fields=('name_image', 'new_time')
    list_display=('name_image', 'new_time', 'showimages')
    readonly_fields=('new_time', 'showimages', 'date')
    list_filter = ('date',)
    search_fields = ['date']

admin.site.register(ImageData, ImageDataAdmin)