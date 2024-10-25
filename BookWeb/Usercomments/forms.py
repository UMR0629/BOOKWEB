from django import forms
from .models import Review,Book

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        labels = {
            'rating':'评分',
            'comment':'评分理由',

        }
class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'average_rating','total_numbers']

class BookReviewForm(forms.Form):
    title = forms.CharField(max_length=200, label='书名')
    rating = forms.FloatField(label='评分')
    comment = forms.CharField(widget=forms.Textarea, label='评分理由')