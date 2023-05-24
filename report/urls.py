from django.urls import path
from . import views
<<<<<<< HEAD
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('home/', views.home_view, name='home'),

    path('api_imagedata/<str:filename>/', views.image_view, name='image_view'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
=======


urlpatterns = [
    path('home/', views.home_view, name='home'),
    path('dashboard/', views.dashboard_now, name='dashboard'),
]
>>>>>>> origin/master
