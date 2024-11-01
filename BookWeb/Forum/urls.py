from django.urls import path
from Forum import views

app_name = 'Forum'
urlpatterns = [
    path('', views.home, name='home'),
    path('new_topic/', views.new_topic, name='new_topic'),
    path('topics/<int:pk>/', views.topic_posts, name='topic_posts'),
    path('topics/<int:pk>/reply/', views.reply_topic, name='reply'),
    path('topics/groups/<int:pk>/', views.gtopic_posts, name='group_posts'),
    path('new_topic/group/',views.new_gtopic,name='new_group_topic'),
    path('topics/groups/<int:pk>/reply/', views.reply_gtopic, name='group_reply'),
    path('home/group/<int:gpk>/',views.Ghome,name='group_home')
]