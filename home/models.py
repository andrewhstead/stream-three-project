# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from tinymce.models import HTMLField


# Create your models here.
# Creates the messages which can be view by administrators through the admin panel.
class Message(models.Model):
    sender = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    date_sent = models.DateTimeField(auto_now_add=True)
    subject = models.CharField(max_length=100)
    message = HTMLField(blank=True)

    def __unicode__(self):
        return self.sender + " | " + self.subject + " - " + unicode(self.date_sent)


# Creates a list of league sponsors.
class Sponsor(models.Model):
    name = models.CharField(max_length=100)
    logo = models.ImageField(upload_to="images/sponsors", blank=True, null=True)

    def __unicode__(self):
        return self.name
