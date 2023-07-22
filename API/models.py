from datetime import datetime
from django.db import models

class SensorData(models.Model):
    time = models.DateTimeField()
    temperature = models.DecimalField(max_digits=5, decimal_places=2)
    humidity = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.time}: Temperature={self.temperature}, Humidity={self.humidity}"

    def save(self, *args, **kwargs):
        if not self.id:
            # 如果是新的SensorData对象，则设置time字段为当前时间
            self.time = datetime.now()
        super().save(*args, **kwargs)

from django.utils.safestring import mark_safe

class ImageData(models.Model):
    time = models.CharField(max_length=100) #捨去
    image = models.ImageField(verbose_name="上傳圖片", upload_to='images/')
    name_image = models.CharField(verbose_name="圖片名稱", max_length=100)
    new_time = models.DateTimeField(verbose_name="新增日期時間", auto_now=True)
    date = models.DateField(verbose_name="新增日期",auto_now=True)

    def showimages(self):
        href = self.image.url
        try:
            img = mark_safe('<img src="%s" width="156px" height="98px" />' % href)
        except Exception:
            img = ''
        return img

    showimages.allow_tags = True

    class Meta:
        ordering = ['new_time']

class Setting(models.Model):
    onTime = models.CharField(max_length=50)  # 用于保存开灯时间
    offTime = models.CharField(max_length=10)  # 用于保存关灯时间
    date = models.DateTimeField(auto_now=True)  # 用于保存日期

    def __str__(self):
        return f'Setting #{self.id}'