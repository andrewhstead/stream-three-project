# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404
from .models import Team, Conference
from news.models import Item
from games.models import Game, get_standings
from forum.views import Board
from datetime import datetime


# Create your views here.
def team_index(request):
    conferences = Conference.objects.all()
    return render(request, "teams.html", {'conferences': conferences})


def team_page(request, team_name):

    current_season = datetime.now().year

    team = get_object_or_404(Team, geographic_name=team_name.capitalize())
    conference = team.conference
    items = Item.objects.filter(teams=team.id).order_by('-created_date')

    games = Game.objects.filter(game_date__year=current_season).order_by('game_date')
    team_results = []
    team_fixtures = []

    standings = get_standings(current_season)

    board = get_object_or_404(Board, team=team)

    for game in games:
        if game.home_team == team or game.away_team == team:
            if game.game_status == "Completed":
                team_results.append(game)
            if game.game_status == "Scheduled":
                team_fixtures.append(game)

    if games:
        last_game = team_results[-1]
        next_game = team_fixtures[0]

        return render(request, "team_profile.html", {'team': team, 'items': items, 'board': board,
                                                     'next_game': next_game, 'last_game': last_game,
                                                     'standings': standings, 'conference': conference})

    else:
        return render(request, "team_profile.html", {'team': team, 'items': items,
                                                     'board': board, 'standings': standings})