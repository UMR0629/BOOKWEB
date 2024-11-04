import os
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from .models import Book, Review
from django.urls import reverse
from django.db.models import Avg
from statistics import mean
from django.core.files.images import ImageFile
from .forms import ReviewForm,BookForm,BookReviewForm
from django.http import HttpResponse, Http404
import statistics

import re
from UserAuth.utils.generateCode import send_sms_code
from UserAuth.utils import validators
from UserAuth.models import User
from UserInfo.models import Resume
# Create your views here.

def book_review(request, book_id):
    user_name = request.session['UserInfo'].get("username")  
    book = get_object_or_404(Book, pk=book_id)
    reviews = book.reviews.all()
    form = None
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.book = book
            review.commenter = user_name
            review.save()
            # 更新书籍的平均评分和总评分人数
            ratings = [r.rating for r in book.reviews.all()]  # 获取所有评分
            if ratings:  # 确保有评分
                book.average_rating = statistics.mean(ratings)  # 计算平均评分
            else:
                book.average_rating = 0.0  # 如果没有评分，设置为 0
            book.total_numbers = book.reviews.count()
            book.save()
            return redirect('Usercomments:book_list')
    else:
        form = ReviewForm()

    return render(request, 'book_review.html', {
        'book': book,
        'reviews': reviews,
        'form': form,
    })

def add_book(request):
    if request.method == 'POST':
        user_name = request.session['UserInfo'].get("username")
        title = request.POST.get('title')
        author = request.POST.get('author','Unknown')
        rating_str = request.POST.get('rating')
        comment = request.POST.get('comment')
        image = request.FILES.get('image')
        try:
            rating = float(rating_str)
        except (ValueError, TypeError):
            # 如果转换失败，返回错误信息或处理错误
            return HttpResponse("评分必须是有效的数字。", status=400)

        if title and rating and comment:
            book, created = Book.objects.get_or_create(title=title,defaults={'author':author})
            if not created and book.author == 'Unknown' and author:
                book.author = author
            if image:
                book.image = image  # 更新图片字段
            if created:
                #book.author = author #初始作者姓名}
                book.average_rating = rating  # 初始评分
                book.total_numbers = 1  # 初始评分人数
            else:
                if image and not book.image: # 只有当书籍没有图片时才更新图片
                    book.image.save(image.name,ImageFile(image))
                book.total_numbers += 1
                book.average_rating = ((book.average_rating * (book.total_numbers - 1)) + rating) / book.total_numbers
            book.save()
            Review.objects.create(book=book, commenter = user_name,rating=float(rating), comment=comment)
            return redirect('Usercomments:book_list')  # 重定向到书籍列表页面
    else:
        return render(request, 'add_book.html')

def book_list(request):

    books = Book.objects.all().order_by('-average_rating')  # 获取所有书籍并按平均评分降序排列
    if 'search' in request.GET:
        search_query = request.GET['search']
        books = Book.objects.filter(title__icontains=search_query)
    default_image_path = 'book_images/default.png'
    for book in books:
        if not book.image:
            default_image = open(os.path.join(settings.MEDIA_ROOT, default_image_path), 'rb')
            book.image.save(default_image_path, ImageFile(default_image))
            book.save()
    return render(request, 'book_list.html', {'books': books})