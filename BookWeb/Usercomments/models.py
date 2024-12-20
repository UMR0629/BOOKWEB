from django.db import models
from UserAuth.models import User
# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=200)  # 书名
    author = models.CharField(max_length=10,default='Unknown')  #作者
    average_rating = models.FloatField(default = 0.0)     # 平均评分
    total_numbers = models.IntegerField(default = 0)    # 总评分人数
    image = models.ImageField(upload_to = 'book_images/',default = 'default.png',blank=True,null=True)

    def __str__(self):
        return self.title

class Review(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews')
    rating = models.FloatField()  # 评分
    comment = models.TextField()  # 评分理由
    commenter = models.CharField(verbose_name="用户名", max_length=32,default="未知用户")
    

