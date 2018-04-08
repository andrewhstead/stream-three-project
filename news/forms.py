from django import forms
from .models import Item


class NewBlogPostForm(forms.ModelForm):

    class Meta:
        model = Item
        fields = ['title', 'cover_image', 'content', 'content_image']