from django.http import HttpResponse
from django.shortcuts import render, redirect

from API import models

def home_view(request):

    return render(request, 'home.html')


from django.shortcuts import render, redirect

def dashboard_now(request):
    TH = models.SensorData.objects.all().order_by('-id')
    if request.method == "POST":
        # 其他處理邏輯

        last_data = 'TH[0]'
        return render(request, 'dashboard.html', {'last_data': last_data})

    # 或者根據需要，重定向到其他頁面
    # return redirect('other_view')

    # 如果沒有明確的返回語句，確保返回一個預設的HttpResponse對象
    return HttpResponse('Error,87')