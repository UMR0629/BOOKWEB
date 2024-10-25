from django.urls import path
from .views import book_list,add_book,book_review
from .import views

app_name = 'comments'

urlpatterns = [
    path('', book_list, name='book_list'),
    path('book/<int:book_id>/review/', book_review, name='book_review'),
    path('add/', add_book, name = 'add_book'),
] 