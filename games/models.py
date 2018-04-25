# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from teams.models import Team
from datetime import datetime

# The options for game status which are available in the administration area.
STATUS_OPTIONS = (
    ('Scheduled', "Scheduled"),
    ('Postponed', "Postponed"),
    ('In Progress', "In Progress"),
    ('Suspended', "Suspended"),
    ('Completed', "Completed"),
)

# The options for game type which are available in the administration area.
TYPE_OPTIONS = (
    ('Pre-Season', "Pre-Season"),
    ('Regular Season', "Regular Season"),
    ('Postseason', "Postseason"),
)


# The function which creates the league standings.
def get_standings(year):

    teams = Team.objects.all().order_by('geographic_name')

    # Empty list to contain the standings
    standings = []

    for team in teams:
        # For each team, create a dictionary with statistics set to 0. Use float rather than integer to facilitate
        # later calculations and number formatting.
        team_record = {"name": team.geographic_name, "abbreviation": team.abbreviation,
                       "conference": team.conference, "small_logo": team.small_logo,
                       "played": 0.0, "won": 0.0, "lost": 0.0,
                       "home_won": 0.0, "home_lost": 0.0,
                       "away_won": 0.0, "away_lost": 0.0,
                       "runs_for": 0.0, "runs_against": 0.0}

        # Next get the team's completed home games and away games for the current year.
        home_games = Game.objects.filter(game_date__year=year).filter(home_team=team)\
            .filter(game_status='Completed').filter(game_type='Regular Season')
        away_games = Game.objects.filter(game_date__year=year).filter(away_team=team)\
            .filter(game_status='Completed').filter(game_type='Regular Season')

        # For each home game, add the game result and score to their record.
        for game in home_games:
            team_record["played"] += 1
            team_record["runs_for"] += game.home_team_runs
            team_record["runs_against"] += game.away_team_runs
            if game.home_team_runs > game.away_team_runs:
                team_record["home_won"] += 1
                team_record["won"] += 1
            if game.home_team_runs < game.away_team_runs:
                team_record["home_lost"] += 1
                team_record["lost"] += 1

        # For each away game, add the game result and score to their record.
        for game in away_games:
            team_record["played"] += 1
            team_record["runs_for"] += game.away_team_runs
            team_record["runs_against"] += game.home_team_runs
            if game.away_team_runs > game.home_team_runs:
                team_record["away_won"] += 1
                team_record["won"] += 1
            if game.away_team_runs < game.home_team_runs:
                team_record["away_lost"] += 1
                team_record["lost"] += 1

        # To prevent zero-division error when no games played, set the team's winning percentage to 0.
        if team_record["played"] == 0:
            team_record["pct"] = 0
        # When games have been played, calculate the winning percentage from the win-loss record.
        else:
            team_record["pct"] = team_record["won"] / team_record["played"]

        # Calculate the difference between the runs scored and allowed by the team.
        team_record["net_runs"] = team_record["runs_for"] - team_record["runs_against"]
        # Add the team's updated record to the standings.
        standings.append(team_record)

    return standings


# Create your models here.
# Creates an object for each season in the league's history. Options run from 2000 (the first season) to the current
# year. The model contains information about the outcome of the season which will be used in creating the archive views.
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


# The main game model. Includes game date, time, status and type, as well as score information. The 'is_premium'
# field allows the game to be chosen for live streaming.
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
    is_premium = models.BooleanField(default=False)

    def __unicode__(self):
        return unicode(self.game_date) + ': ' + unicode(self.away_team) + ' @ ' + unicode(self.home_team)
