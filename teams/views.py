# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404
from .models import Team, Conference
from news.models import Item
from games.models import Game
from games.views import current_season
from forum.views import Board


# Create your views here.
def team_index(request):
    conferences = Conference.objects.all()
    return render(request, "teams.html", {'conferences': conferences})


def team_page(request, team_name):
    items = Item.objects.all()
    team = get_object_or_404(Team, geographic_name=team_name.capitalize())

    games = Game.objects.filter(game_date__year=current_season).order_by('game_date')
    team_results = []
    team_fixtures = []

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
                                                     'next_game': next_game, 'last_game': last_game})

    else:
        return render(request, "team_profile.html", {'team': team, 'items': items, 'board': board})
