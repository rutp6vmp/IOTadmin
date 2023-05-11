# Generated by Django 4.2.1 on 2023-05-24 05:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("API", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="ImageData",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("time", models.CharField(max_length=100)),
                ("image", models.ImageField(upload_to="images/")),
                ("name_image", models.CharField(max_length=100)),
            ],
        ),
    ]
