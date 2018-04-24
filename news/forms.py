from django import forms
from .models import Item, Comment


# Form to submit a new blog post.
class BlogPostForm(forms.ModelForm):

    class Meta:
        model = Item
        fields = ['title', 'cover_image', 'content', 'content_image']


# Form to comment on a news story or blog post.
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']
