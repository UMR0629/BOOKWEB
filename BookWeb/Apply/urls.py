from django.urls import path
from Apply import views


app_name = 'Apply'
urlpatterns = [
    path("apply/", views.create, name='apply'),
]