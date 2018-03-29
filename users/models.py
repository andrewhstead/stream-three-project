# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from teams.models import Team


# Create your models here.
class User(AbstractUser):
    objects = UserManager
    profile_picture = models.ImageField(upload_to="images/users", blank=True, null=True)
    favourite_team = models.ForeignKey(Team, related_name="user", blank=True, null=True)

    def __unicode__(self):
        return self.username
