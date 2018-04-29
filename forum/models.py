# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from tinymce.models import HTMLField
from users.models import User
from teams.models import Team


# Create your models here.
# A section within the forum - used to categorise the boards.
class Section(models.Model):
    title = models.CharField(max_length=50)

    def __unicode__(self):
        return self.title


# The individual boards within the forum. Can be linked to a specific team or be general league-wide boards.
class Board(models.Model):
    title = models.CharField(max_length=50)
    section = models.ForeignKey(Section, related_name='boards')
    team = models.ForeignKey(Team, related_name='board', blank=True, null=True)
    thread_count = models.IntegerField(default=0)
    post_count = models.IntegerField(default=0)
    description = HTMLField(blank=True)

    def __unicode__(self):
        return self.title


# A thread in the forum. Attributed to the user who created the thread and allocated to the relevant board. The
# 'last_post' field will be updated every time a post is added or deleted.
class Thread(models.Model):
    title = models.CharField(max_length=50)
    user = models.ForeignKey(User, related_name='threads')
    board = models.ForeignKey(Board, related_name='threads')
    created_date = models.DateTimeField(auto_now_add=True)
    post_count = models.IntegerField(default=0)
    last_post = models.DateTimeField(auto_now_add=True)
    views = models.IntegerField(default=0)

    def __unicode__(self):
        return self.title


# An individual forum post, attributed to a user an allocated to the relevant thread.
class Post(models.Model):
    user = models.ForeignKey(User, related_name='posts')
    thread = models.ForeignKey(Thread, related_name='posts')
    board = models.ForeignKey(Board, related_name='posts')
    content = HTMLField(blank=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return unicode(self.thread) + "; " + unicode(self.user)
