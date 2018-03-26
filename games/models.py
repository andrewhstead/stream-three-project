# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from teams.models import Team

STATUS_OPTIONS = (
    ('Scheduled', "Scheduled"),
    ('Postponed', "Postponed"),
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
    game_status = models.CharField(max_length=10, choices=STATUS_OPTIONS, default="Scheduled")
    game_type = models.CharField(max_length=15, choices=TYPE_OPTIONS, default="Regular Season")
    home_team = models.ForeignKey(Team, related_name='game_home')
    away_team = models.ForeignKey(Team, related_name='game_away')
    innings = models.IntegerField(default=9)
    home_team_runs = models.IntegerField(blank=True, null=True)
    home_team_hits = models.IntegerField(blank=True, null=True)
    home_team_errors = models.IntegerField(blank=True, null=True)
    away_team_runs = models.IntegerField(blank=True, null=True)
    away_team_hits = models.IntegerField(blank=True, null=True)
    away_team_errors = models.IntegerField(blank=True, null=True)
    attendance = models.IntegerField(blank=True, null=True)

    def __unicode__(self):
        return unicode(self.game_date) + ': ' + unicode(self.home_team) + ' v ' + unicode(self.away_team)
