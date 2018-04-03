# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from teams.models import Team
from datetime import datetime

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
class Season(models.Model):
    SEASON_OPTIONS = (
        (year, year) for year in range(2000, datetime.now().year+1)
    )

    year = models.IntegerField(choices=SEASON_OPTIONS)
    schedule_length = models.IntegerField(default=60)
    champion = models.ForeignKey(Team, related_name='champion', blank=True, null=True)
    series_score = models.CharField(max_length=3, blank=True, null=True)
    finalist = models.ForeignKey(Team, related_name='finalist', blank=True, null=True)

    def __unicode__(self):
        return unicode(self.year)


class Game(models.Model):
    season = models.ForeignKey(Season, related_name='games', default=datetime.now().year)
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
