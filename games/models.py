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


def get_standings(year):

    teams = Team.objects.all().order_by('geographic_name')
    games = Game.objects.filter(game_date__year=year)\
        .filter(game_type="Regular Season").filter(game_status="Completed")
    standings = []

    for team in teams:
        team_record = {"name": team.geographic_name, "abbreviation": team.abbreviation,
                       "conference": team.conference, "small_logo": team.small_logo,
                       "played": 0.0, "won": 0.0, "lost": 0.0,
                       "home_won": 0.0, "home_lost": 0.0,
                       "away_won": 0.0, "away_lost": 0.0,
                       "runs_for": 0.0, "runs_against": 0.0}
        for game in games:
            if game.home_team == team:
                team_record["played"] += 1
                team_record["runs_for"] += game.home_team_runs
                team_record["runs_against"] += game.away_team_runs
                if game.home_team_runs > game.away_team_runs:
                    team_record["home_won"] += 1
                    team_record["won"] += 1
                if game.home_team_runs < game.away_team_runs:
                    team_record["home_lost"] += 1
                    team_record["lost"] += 1
            elif game.away_team == team:
                team_record["played"] += 1
                team_record["runs_for"] += game.away_team_runs
                team_record["runs_against"] += game.home_team_runs
                if game.away_team_runs > game.home_team_runs:
                    team_record["away_won"] += 1
                    team_record["won"] += 1
                if game.away_team_runs < game.home_team_runs:
                    team_record["away_lost"] += 1
                    team_record["lost"] += 1
        if team_record["played"] == 0:
            team_record["pct"] = 0  # To prevent zero-division error when no games played.
        else:
            team_record["pct"] = team_record["won"] / team_record["played"]
        team_record["net_runs"] = team_record["runs_for"] - team_record["runs_against"]
        standings.append(team_record)

    return standings


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
    is_premium = models.BooleanField()

    def __unicode__(self):
        return unicode(self.game_date) + ': ' + unicode(self.away_team) + ' @ ' + unicode(self.home_team)
