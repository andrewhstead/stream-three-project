# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404
from .models import Game
from teams.models import Team, Conference


# Create your views here.
def last_and_next(request):

    all_results = Game.objects.filter(game_status="Completed").order_by('game_date')
    result_dates = []

    for result in all_results:
        if result.game_date not in result_dates:
            result_dates.append(result.game_date)

    latest_date = result_dates[-1]
    latest_results = all_results.filter(game_date=latest_date).order_by('home_team')

    all_fixtures = Game.objects.filter(game_status="Scheduled").order_by('game_date')
    fixture_dates = []

    for fixture in all_fixtures:
        if fixture.game_date not in fixture_dates:
            fixture_dates.append(fixture.game_date)

    next_date = fixture_dates[0]
    next_fixtures = all_fixtures.filter(game_date=next_date).order_by('home_team')

    return render(request, "games.html", {"results": latest_results, "fixtures": next_fixtures,
                                          "latest_date": latest_date, "next_date": next_date})


def league_standings(request):
    conferences = Conference.objects.all()
    teams = Team.objects.all().order_by('geographic_name')
    games = Game.objects.filter(game_status="Completed")
    standings = []

    for team in teams:
        team.record = {"name": team.geographic_name, "conference": team.conference,
                       "small_logo": team.small_logo, "played": 0.0, "won": 0.0, "lost": 0.0}
        for game in games:
            if game.home_team == team:
                team.record["played"] += 1
                if game.home_team_runs > game.away_team_runs:
                    team.record["won"] += 1
                if game.home_team_runs < game.away_team_runs:
                    team.record["lost"] += 1
            elif game.away_team == team:
                team.record["played"] += 1
                if game.away_team_runs > game.home_team_runs:
                    team.record["won"] += 1
                if game.away_team_runs < game.home_team_runs:
                    team.record["lost"] += 1
        team.record["pct"] = team.record["won"] / team.record["played"]
        standings.append(team.record)

    return render(request, "standings.html", {"conferences": conferences, "teams": teams,
                                              "games": games, "standings": standings})


def games_team(request, team_name):
    games = Game.objects.all().order_by('game_date')
    team = get_object_or_404(Team, geographic_name=team_name.capitalize())
    team_schedule = []

    for game in games:
        if game.home_team == team:
            game.team = game.home_team
            game.opponent = game.away_team
            game.team_runs = game.home_team_runs
            game.opponent_runs = game.away_team_runs
            team_schedule.append(game)
        elif game.away_team == team:
            game.team = game.away_team
            game.opponent = game.home_team
            game.team_runs = game.away_team_runs
            game.opponent_runs = game.home_team_runs
            team_schedule.append(game)

    return render(request, "games_team.html", {"team": team, "team_games": team_schedule})
