# Generated by Django 4.2 on 2023-07-22 08:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('API', '0007_setting'),
    ]

    operations = [
        migrations.AddField(
            model_name='setting',
            name='date',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
