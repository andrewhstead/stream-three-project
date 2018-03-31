# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from teams.models import Team

STATUS_OPTIONS = (
    ('Scheduled', "Scheduled"),
    ('Postponed', "Postponed"),
    ('In Progress', "In Progress"),
    ('Suspended', "Suspended"),
    ('Completed', "Completed"),
)

TYPE_OPTIONS = (
    ('Pre-Season', "Pre-Season"),
    ('Regular Season', "Regular Season"),
    ('Postseason', "Postseason"),
)


# Create your models here.
class Game(models.Model):
    game_date = models.DateField()
    game_time = models.TimeField()
    game_status = models.CharField(max_length=15, choices=STATUS_OPTIONS, default="Scheduled")
    game_type = models.CharField(max_length=15, choices=TYPE_OPTIONS, default="Regular Season")
    away_team = models.ForeignKey(Team, related_name='away')
    home_team = models.ForeignKey(Team, related_name='home')
    innings = models.IntegerField(default=9)
    away_team_runs = models.IntegerField(blank=True, null=True)
    away_team_hits = models.IntegerField(blank=True, null=True)
    away_team_errors = models.IntegerField(blank=True, null=True)
    home_team_runs = models.IntegerField(blank=True, null=True)
    home_team_hits = models.IntegerField(blank=True, null=True)
    home_team_errors = models.IntegerField(blank=True, null=True)
    attendance = models.IntegerField(blank=True, null=True)

    def __unicode__(self):
        return unicode(self.game_date) + ': ' + unicode(self.away_team) + ' @ ' + unicode(self.home_team)


class Season(models.Model):
    year = models.IntegerField()
    champion = models.ForeignKey(Team, related_name='champion', blank=True, null=True)
    finalist = models.ForeignKey(Team, related_name='finalist', blank=True, null=True)
    games = models.IntegerField(default=0)
    runs_per_game = models.FloatField(default=0)

    def __unicode__(self):
        return unicode(self.year)
