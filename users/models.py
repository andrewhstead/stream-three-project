# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from teams.models import Team


# Create your models here.
class User(AbstractUser):
    objects = UserManager()
    stripe_id = models.CharField(max_length=40, default='')
    subscription_ends = models.DateTimeField(blank=True, null=True)
    subscription_renews = models.BooleanField(default=False)
    subscription_plan = models.CharField(max_length=25, blank=True, null=True)
    is_private = models.BooleanField(default=False)
    profile_picture = models.ImageField(upload_to="images/users", blank=True, null=True)
    favourite_team = models.ForeignKey(Team, related_name="user", blank=True, null=True)

    def __unicode__(self):
        return self.username
