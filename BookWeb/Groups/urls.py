from django.urls import path
from Groups import views


app_name = 'Groups'
urlpatterns = [
    path("create/", views.create, name='create_group'),
    path("show/", views.show, name='show_group'),
    path("group/<int:pk>/", views.index, name='group'),
    path("apply/<int:pk>/",views.showapplications,name='applicants'),
    path('add/<int:gid>/<str:theapplicant>', views.manage, name='addmember'),
    path('delete/<str:name>/<str:applicant>', views.delete, name='delete'),
]