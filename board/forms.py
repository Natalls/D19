from django import forms
from .models import Post, Reply

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'title',
            'post_text',
            'category',
        ]
        labels = {
            'title': 'Заголовок',
            'post_text': '',
            'category': 'Категория',
        }


class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = [
            'reply_text',
        ]
        labels = {
            'reply_text': ''
        }