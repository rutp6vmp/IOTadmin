from django.contrib import admin
from API.models import *

class ImageDataAdmin(admin.ModelAdmin):
    fields=('name_image', 'new_time', 'image')
    list_display=('name_image', 'new_time', 'showimages', 'image')
    readonly_fields=('new_time', 'date')
    list_filter = ('date',)
    search_fields = ['date']
    #list_per_page = 20

admin.site.register(ImageData, ImageDataAdmin)
#hello