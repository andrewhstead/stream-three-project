# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


# Create your models here.
class Team(models.Model):
    geographic_name = models.CharField(max_length=100)
    nickname = models.CharField(max_length=100)
    abbreviation = models.CharField(max_length=5)
    conference = models.CharField(max_length=25)
    ballpark = models.CharField(max_length=100)
    large_logo = models.ImageField(upload_to="images/teams/logos", blank=True, null=True)
    small_logo = models.ImageField(upload_to="images/teams/logos", blank=True, null=True)
    home_uniform = models.ImageField(upload_to="images/teams/uniforms", blank=True, null=True)
    away_uniform = models.ImageField(upload_to="images/teams/uniforms", blank=True, null=True)

    def __unicode__(self):
        return self.geographic_name + " " + self.nickname