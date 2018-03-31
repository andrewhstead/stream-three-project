# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from users.models import User
from news.models import Item
from tinymce.models import HTMLField


# Create your models here.
class Comment(models.Model):
    user = models.ForeignKey(User, related_name='comments')
    item = models.ForeignKey(Item, related_name='comments')
    comment = HTMLField(blank=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.item.title + " | " + self.user.username
