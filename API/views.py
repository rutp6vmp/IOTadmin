from .models import *
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import permissions
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView
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
用途 :測試寫入溫濕度
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

"""
API_3:save-sensor-data
用途 :寫入圖片
POST
"""
# @api_view(['POST'])
# @swagger_auto_schema(
#     request_body=openapi.Schema(
#         type=openapi.TYPE_OBJECT,
#         required=['time', 'image', 'name_image'],
#         properties={
#             'time': openapi.Schema(type=openapi.TYPE_STRING, description='date and time'),
#             'image': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_BINARY, description='Image file'),
#             'name_image': openapi.Schema(type=openapi.TYPE_STRING, description='Image name'),
#         },
#     ),
#     operation_description='Save image data',
#     responses={
#         '200': 'OK',
#         '400': 'Bad request',
#     },
# )

# def save_image_data(request):
#     if request.method == 'POST':
#
#         time = request.data.get('time')
#         image = request.data.get('image')
#         name_image = request.data.get('name_image')
#
#         # 处理图像的逻辑，例如保存到文件系统或云存储
#         image_data = ImageData(time=time, image=image, name_image=name_image)
#         image_data.save()
#
#         return Response(status=200)
#     else:
#         return Response(status=400)
#

@swagger_auto_schema(
    method='post',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['time', 'image', 'name_image'],
        properties={
            'time': openapi.Schema(type=openapi.TYPE_STRING, description='date and time'),
            'image': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_BINARY, description='Image file'),
            'name_image': openapi.Schema(type=openapi.TYPE_STRING, description='Image name'),
        },
    ),
    operation_description='Upload image',
    responses={
        '200': 'OK',
        '400': 'Bad request',
    },
)
@api_view(['POST'])
def upload_image(request):
    if request.method == 'POST':

        time = request.data.get('time')
        image = request.data.get('image')
        name_image = request.data.get('name_image')

        # 处理图像的逻辑，例如保存到文件系统或云存储
        image_data = ImageData(time=time, image=image, name_image=name_image)
        image_data.save()

        return Response(status=200)
    else:
        return Response(status=400)



"""
API框架共用檔案
"""
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

