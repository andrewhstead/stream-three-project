# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404
from .models import Team, Conference
from news.models import Item
from games.models import Game
from datetime import datetime


# Create your views here.
def team_index(request):
    conferences = Conference.objects.all()
    return render(request, "teams.html", {'conferences': conferences})


def team_page(request, team_name):
    items = Item.objects.all()
    team = get_object_or_404(Team, geographic_name=team_name.capitalize())

    games = Game.objects.filter(game_date__year=datetime.now().year).order_by('game_date')
    team_results = []
    team_fixtures = []

    for game in games:
        if game.home_team == team or game.away_team == team:
            if game.game_status == "Completed":
                team_results.append(game)
            if game.game_status == "Scheduled":
                team_fixtures.append(game)

    last_game = team_results[-1]
    next_game = team_fixtures[0]

    return render(request, "profile.html", {'team': team, 'items': items,
                                            'next_game': next_game, 'last_game': last_game})
