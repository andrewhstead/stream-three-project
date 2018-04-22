from django import forms
from .models import Item, Comment


class BlogPostForm(forms.ModelForm):

    class Meta:
        model = Item
        fields = ['title', 'cover_image', 'content', 'content_image']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']
