from .models import *
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import permissions
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import render, redirect
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

from django.views.generic import TemplateView
class showimage(TemplateView):
    template_name = 'image.html'

    def get(self, request, *args, **kwargs): 
        images=ImageData.objects.all()
        context=self.get_context_data(**kwargs)
        context['items'] = images

        return self.render_to_response(context)
    
class index(TemplateView):
    template_name = 'index.html'

    def get(self, request, *args, **kwargs): 
        images=ImageData.objects.order_by('-new_time')[:10]
        context=self.get_context_data(**kwargs)
        context['items'] = images

        return self.render_to_response(context)
    
from django.db.models import Q

class history(TemplateView):
    template_name = 'history.html'

    def get(self, request, *args, **kwargs): 
        date = request.GET.get('date')
        search = request.GET.get('search')
        
        images = ImageData.objects.all()
        
        if date:
            images = images.filter(date=date)
        
        if search:
            images = images.filter(Q(name_image__icontains=search))
        
        context = self.get_context_data(**kwargs)
        context['items'] = images

        return self.render_to_response(context)

# from django.contrib import messages
# import time
# from datetime import datetime, time as dt_time
# from serial import Serial
# import serial
# import modbus_tk.modbus_rtu as modbus_rtu
# import modbus_tk.defines as cst
# from django.contrib.messages import get_messages

# def setTime(request):
#     mbComPort = '/dev/ttyUSB0'#'3COM7'   # COM3->RS-485
#     baudrate = 9600
#     databit = 8
#     parity = 'N'
#     stopbit = 1
#     mbTimeout = 100 # ms

#     def control_light(value):
#         mb_port = serial.Serial(port=mbComPort, baudrate=baudrate, bytesize=databit, parity=parity, stopbits=stopbit)
#         master = modbus_rtu.RtuMaster(mb_port)
#         master.set_timeout(mbTimeout/1000.0)

#         mbId = 1
#         addr = 2 #base0

#         try:
#             #-- FC5: write multi-coils
#             rr = master.execute(mbId, cst.WRITE_SINGLE_COIL, addr, output_value=value)
#             print("Write(addr, value)=%s" %(str(rr)))
#             message = "設定成功"
#             messages.success(request, message)
#         except Exception as e:
#             print("modbus test Error: " + str(e))
#             message = "設定失敗：" + str(e)
#             messages.error(request, message)

#         master._do_close()


#     def set_light_on_off(start_time, end_time, request):
#             while True:
#                 current_time = datetime.now().time()  # 获取当前时间

#                 if start_time <= current_time <= end_time:
#                     # 在指定时间范围内，开启灯光
#                     control_light(1)
#                 else:
#                     # 不在指定时间范围内，关闭灯光
#                     control_light(0)

#                 # 计算距离下一个完整分钟的时间间隔
#                 current_second = datetime.now().second
#                 sleep_time = 60 - current_second

#                 time.sleep(sleep_time)  # 等待到下一个完整分钟

#                 messages = get_messages(request)
#                 for message in messages:
#                     messages.add(message)  # 将消息添加到模板上下文中    


#     if request.method == 'POST':
#         onTime = request.POST.get('onTime')
#         offTime = request.POST.get('offTime')

#         on_hour, on_minute = onTime.split(':')
#         off_hour, off_minute = offTime.split(':')

#         start_time = dt_time(int(on_hour), int(on_minute))   # 设置开启时间为每天8点
#         end_time = dt_time(int(off_hour), int(off_minute))    # 设置关闭时间为每天18点

#         set_light_on_off(start_time, end_time, request)  # 调用函数来设置每日按照指定时间开启和关闭灯光

#         return redirect(request.META.get('HTTP_REFERER'))
    

#     message = None
#     return render(request, 'setTime.html', {'message': message})