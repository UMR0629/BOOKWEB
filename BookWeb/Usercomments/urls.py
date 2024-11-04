from django.urls import path
from .views import book_list,add_book,book_review
from .import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'Usercomments'

urlpatterns = [
    
    path('', book_list, name='book_list'),
    path('book/<int:book_id>/review/', book_review, name='book_review'),
    path('add/', add_book, name = 'add_book'),
] 