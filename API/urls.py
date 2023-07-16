# from django.urls import path
# from .views import *
#
# urlpatterns = [
#
#     path('hello/', hello_world, name='hello_world'),
#     path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
#     path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
#     path('save-sensor-data/', save_sensor_data, name='save_sensor_data'),
# ]
from django.urls import path
from . import views
from .views import *
from rest_framework.schemas import get_schema_view
from rest_framework import permissions
from drf_yasg.views import get_schema_view as get_swagger_view
from drf_yasg import openapi
from django.conf import settings
from django.conf.urls.static import static

schema_view = get_swagger_view(
    openapi.Info(
        title="My API",
        default_version='v1',
        description="API description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@mysite.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('hello/', hello_world, name='hello_world'),
    path('save-sensor-data/', save_sensor_data, name='save_sensor_data'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('upload_image/', upload_image, name='upload_image'),
    path('image/', views.showimage.as_view(), name='image'), 
    path('index/', views.index.as_view(), name='index'), 
    path('history/', views.history.as_view(), name='history'), 
    # path('setTime/', views.setTime, name='setTime'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
