# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from tinymce.models import HTMLField


# Create your models here.
class Message(models.Model):
    sender = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    date_sent = models.DateTimeField(auto_now_add=True)
    subject = models.CharField(max_length=100)
    message = HTMLField(blank=True)

    def __unicode__(self):
        return self.sender + " | " + self.subject + " - " + unicode(self.date_sent)
