from django import forms
from .models import Message


# Form to send a message to the site adminstrator.
class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['sender', 'email', 'subject', 'message']
        labels = {
            'sender': 'Name',
        }
