# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from teams.models import Team
from users.models import User
from games.models import Game
from tinymce.models import HTMLField
from django.contrib.auth.models import Group


def list_bloggers():

    blogger = Group.objects.get(name='Blogger')
    bloggers = []

    users = User.objects.all()
    for user in users:
        if blogger in user.groups.all():
            bloggers.append(user)

    return bloggers


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=50)
    default_image = models.ImageField(upload_to="images/news/categories")

    def __unicode__(self):
        return self.name


class Item(models.Model):
    author = models.ForeignKey(User, related_name='news', default='Admin')
    title = models.CharField(max_length=200)
    cover_image = models.ImageField(upload_to="images/news/covers", blank=True, null=True)
    content = HTMLField()
    content_image = models.ImageField(upload_to="images/news/content", blank=True, null=True)
    image_caption = models.CharField(max_length=100, blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, related_name='item')
    teams = models.ManyToManyField(Team, related_name="item", blank=True)
    views = models.IntegerField(default=0)
    published_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __unicode__(self):
        return self.title


class Comment(models.Model):
    user = models.ForeignKey(User, related_name='comments')
    item = models.ForeignKey(Item, related_name='comments')
    comment = HTMLField(blank=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.item.title + " | " + self.user.username
