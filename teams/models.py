# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


# Create your models here.
# Sets the basic information about the league.
class League(models.Model):
    name = models.CharField(max_length=100)
    abbreviation = models.CharField(max_length=5)
    logo = models.ImageField(upload_to="images/league", blank=True, null=True)
    default_image = models.ImageField(upload_to="images/users", blank=True, null=True)

    def __unicode__(self):
        return self.name


# Sets the league structure by defining the conferences.
class Conference(models.Model):
    name = models.CharField(max_length=100)
    short_name = models.CharField(max_length=10)
    abbreviation = models.CharField(max_length=3)

    def __unicode__(self):
        return self.name


# Sets up a team and their associated images.
class Team(models.Model):
    geographic_name = models.CharField(max_length=100)
    nickname = models.CharField(max_length=100)
    abbreviation = models.CharField(max_length=5)
    conference = models.ForeignKey(Conference, related_name='teams')
    ballpark = models.CharField(max_length=100)
    large_logo = models.ImageField(upload_to="images/teams/logos", blank=True, null=True)
    small_logo = models.ImageField(upload_to="images/teams/logos", blank=True, null=True)
    home_uniform = models.ImageField(upload_to="images/teams/uniforms", blank=True, null=True)
    away_uniform = models.ImageField(upload_to="images/teams/uniforms", blank=True, null=True)
    alternate_uniform = models.ImageField(upload_to="images/teams/uniforms", blank=True, null=True)

    def __unicode__(self):
        return self.geographic_name + " " + self.nickname
