# Generated by Django 4.2.5 on 2024-10-28 03:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Usercomments', '0003_remove_book_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='author',
            field=models.CharField(default='Unkown', max_length=10),
        ),
    ]
