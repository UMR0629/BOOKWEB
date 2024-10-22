# Generated by Django 4.2.16 on 2024-10-22 05:18

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("UserAuth", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="user",
            name="excepting_location",
        ),
        migrations.RemoveField(
            model_name="user",
            name="excepting_position",
        ),
        migrations.AddField(
            model_name="user",
            name="maxim",
            field=models.CharField(blank=True, max_length=30, verbose_name="格言"),
        ),
        migrations.AddField(
            model_name="user",
            name="my_love_author",
            field=models.CharField(blank=True, max_length=30, verbose_name="最喜爱的作者"),
        ),
        migrations.AddField(
            model_name="user",
            name="my_love_book",
            field=models.CharField(blank=True, max_length=30, verbose_name="最喜爱的书籍"),
        ),
    ]
