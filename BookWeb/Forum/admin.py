from django.contrib import admin
from .models import Topic, Post,GTopic
# Register your models here.

admin.site.register(Topic)
admin.site.register(Post)
admin.site.register(GTopic)