# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from tinymce.models import HTMLField
from users.models import User
from teams.models import Team


# Create your models here.
class Section(models.Model):
    title = models.CharField(max_length=50)

    def __unicode__(self):
        return self.title


class Board(models.Model):
    title = models.CharField(max_length=50)
    section = models.ForeignKey(Section, related_name='boards')
    team = models.ForeignKey(Team, related_name='board', blank=True, null=True)
    description = HTMLField(blank=True)

    def __unicode__(self):
        return self.title


class Thread(models.Model):
    title = models.CharField(max_length=200)
    user = models.ForeignKey(User, related_name='threads')
    board = models.ForeignKey(Board, related_name='threads')
    created_date = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.title


class Post(models.Model):
    user = models.ForeignKey(User, related_name='posts')
    thread = models.ForeignKey(Board, related_name='posts')
    content = HTMLField(blank=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return unicode(self.thread) + "; " + unicode(self.user)
