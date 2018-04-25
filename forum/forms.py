from django import forms
from .models import Thread, Post


# Form to create a new thread in the forum.
class ThreadForm(forms.ModelForm):
    class Meta:
        model = Thread
        fields = ['title']
        labels = {
            'title': 'Thread Title',
        }


# Form to create a new post within a thread.
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content']
        labels = {
            'content': 'Post',
        }
