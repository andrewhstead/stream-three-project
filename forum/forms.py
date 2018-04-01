from django import forms
from .models import Thread, Post


class ThreadForm(forms.ModelForm):
    class Meta:
        model = Thread
        fields = ['title']
        labels = {
            'title': 'Thread Title',
        }


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content']
        labels = {
            'content': 'Post',
        }
