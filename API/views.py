from .models import *
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import permissions
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

"""
API_1:Hello
用途 :測試返回
GET
"""


@api_view(['GET'])
def hello_world(request):
    return Response({'message': 'Hello, World!'})


"""
API_2:save-sensor-data
用途 :測試寫入
POST
"""

@swagger_auto_schema(
    method='post',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['time', 'T', 'H'],
        properties={
            'time': openapi.Schema(type=openapi.TYPE_STRING, description='date and time'),
            'T': openapi.Schema(type=openapi.TYPE_NUMBER, description='temperature'),
            'H': openapi.Schema(type=openapi.TYPE_NUMBER, description='humidity'),
        },
    ),
    operation_description='Save sensor data',
    responses={
        '200': 'OK',
        '400': 'Bad request',
    },
)
@api_view(['POST'])
def save_sensor_data(request):
    if request.method == 'POST':
        data = request.data
        time = data['time']
        temperature = data['T']
        humidity = data['H']
        sensor_data = SensorData(time=time, temperature=temperature, humidity=humidity)
        sensor_data.save()
        return Response(status=200)
    else:
        return Response(status=400)


from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="IOT API",
      default_version='v1',
      description="接收Raspbettr 資料 API",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@myproject.local"),
      license=openapi.License(name="MIT License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

