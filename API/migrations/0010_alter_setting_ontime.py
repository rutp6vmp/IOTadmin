# Generated by Django 4.2 on 2023-07-22 08:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('API', '0009_remove_setting_ontime_2_remove_setting_ontime_3'),
    ]

    operations = [
        migrations.AlterField(
            model_name='setting',
            name='onTime',
            field=models.CharField(max_length=50),
        ),
    ]
