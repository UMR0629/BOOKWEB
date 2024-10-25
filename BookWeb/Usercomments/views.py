from django.shortcuts import render, get_object_or_404, redirect
from .models import Book, Review
from django.urls import reverse
from .forms import ReviewForm,BookForm,BookReviewForm
# Create your views here.

def book_review(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    reviews = book.reviews.all()
    form = None
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.book = book
            review.save()
            # 更新书籍的平均评分和总评分人数
            book.average_rating = book.reviews.aggregate(avg_rating=Avg('rating'))['avg_rating'] or 0
            book.total_numbers = book.reviews.count()
            book.save()
            return redirect('comments:book_review', book.id)
    else:
        form = ReviewForm()

    return render(request, 'book_review.html', {
        'book': book,
        'reviews': reviews,
        'form': form,
    })

def add_book(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        rating_str = request.POST.get('rating')
        comment = request.POST.get('comment')
        try:
            rating = float(rating_str)
        except (ValueError, TypeError):
            # 如果转换失败，返回错误信息或处理错误
            return HttpResponse("评分必须是有效的数字。", status=400)

        if title and rating and comment:
            book, created = Book.objects.get_or_create(title=title)
            if created:
                book.average_rating = rating  # 初始评分
                book.total_numbers = 1  # 初始评分人数
            else:
                book.total_numbers += 1
                book.average_rating = ((book.average_rating * (book.total_numbers - 1)) + rating) / book.total_numbers
            book.save()
            Review.objects.create(book=book, rating=float(rating), comment=comment)
            return redirect('comments:book_list')  # 重定向到书籍列表页面
    else:
        return render(request, 'add_book.html')

def book_list(request):

    books = Book.objects.all().order_by('-average_rating')  # 获取所有书籍并按平均评分降序排列
    if 'search' in request.GET:
        search_query = request.GET['search']
        books = Book.objects.filter(title__icontains=search_query)
    return render(request, 'book_list.html', {'books': books})