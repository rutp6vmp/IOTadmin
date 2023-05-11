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

class ImageData(models.Model):
    time = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images/')
    name_image = models.CharField(max_length=100)
