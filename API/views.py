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


import paho.mqtt.client as mqtt
import time, json, datetime, sys, os
import random
from django.contrib import messages
from API.models import Setting

def setTime(request):
    def on_connect_callback(client, userdata, flags, rc):
        # 回调函数的实现
        m = "Connected flags" + str(flags) + ", result code " + str(rc) + ", client_id  " + str(client)
        print(m)
    
    def on_connect(onTime, offTime):
        broker_address = "broker.hivemq.com"
        broker_port = 1883

        client1 = mqtt.Client()    #create new instance
        client1.on_connect = on_connect_callback        #attach function to callback

        time.sleep(0.5)
        client1.connect(host=broker_address, port=broker_port, keepalive=60)      #connect to broker
                
        client1.loop_start()    #start the loop
        time.sleep(0.5)

        try:
            #-- start to push data
            client1.publish('kh_wetland/on_time', onTime, qos=1)  #msg是訊息內容、topic_str是訊息的key
            time.sleep(0.1)
            client1.publish('kh_wetland/off_time', offTime, qos=1)
            time.sleep(0.1)
            message = "成功"
            messages.success(request, message) 
        except Exception as e:
            message = "發送失敗：" + str(e)
            messages.error(request, message)

        client1.disconnect()


    if request.method == 'POST':
        show_time_list = []

        onTime = request.POST.get('onTime')
        if onTime:
            show_time_list.append(onTime)
        
        newonTime = onTime.replace(':', '')
        newonTime = '["' + newonTime + '"]'
        set_time_list = [newonTime]

        offTime = request.POST.get('offTime')
        if not offTime:
            offTime = None
        else:
            newoffTime = offTime.replace(':', '')
            newoffTime = '["' + newoffTime + '"]'

        onTime_2 = request.POST.get('onTime-2')
        onTime_3 = request.POST.get('onTime-3')

        # 处理第二个时间段
        if onTime_2:
            show_time_list.append(onTime_2)
            newonTime_2 = onTime_2.replace(':', '')
            newonTime_2 = '["' + newonTime_2 + '"]'
            set_time_list.append(newonTime_2)

        # 处理第三个时间段
        if onTime_3:
            show_time_list.append(onTime_3)
            newonTime_3 = onTime_3.replace(':', '')
            newonTime_3 = '["' + newonTime_3 + '"]'
            set_time_list.append(newonTime_3)
        

        # 将列表转换为 JSON 格式的字符串
        onTimes_str = json.dumps(set_time_list)
        

        on_connect(onTimes_str, newoffTime)

        setting = Setting(onTime=show_time_list, offTime=offTime)
        setting.save()
        

        return redirect(request.META.get('HTTP_REFERER'))
    
    else:
        # ids_to_delete = [4, 5]
        # Setting.objects.filter(id__in=ids_to_delete).delete()
        contexts = Setting.objects.all()
        if not contexts:
            contexts = None
        else:
            contexts[0].is_first = True
        message = None

    return render(request, 'setTime.html', {'message': message, 'contexts': contexts})