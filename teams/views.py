# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404
from .models import Team, Conference
from news.models import Item
from store.models import Product
from games.models import Game, get_standings
from forum.views import Board
from datetime import datetime
from django.db.models import Q


# Create your views here.
# Index page showing every team and basic information about them.
def team_index(request):
    conferences = Conference.objects.all()
    return render(request, "teams.html", {'conferences': conferences})


# The team's own profile page.
def team_page(request, team_name):

    current_season = datetime.now().year

    team = get_object_or_404(Team, geographic_name=team_name.capitalize())
    conference = team.conference
    standings = get_standings(current_season)

    # Team specific news, message board and merchandise.
    items = Item.objects.filter(teams=team.id).order_by('-created_date')
    products = Product.objects.filter(team=team)
    board = Board.objects.get(team=team)

    # Find the last game played by the team and the next one they have scheduled.
    team_results = []
    team_fixtures = []

    # The page is not an archive page.
    archive = False

    results = Game.objects.filter(game_date__year=current_season).filter(Q(home_team=team) | Q(away_team=team)).filter(
        game_status='Completed').order_by('game_date')
    fixtures = Game.objects.filter(game_date__year=current_season).filter(Q(home_team=team) | Q(away_team=team)).filter(
        game_status='Scheduled').order_by('game_date')

    for game in results:
        team_results.append(game)
    for game in fixtures:
        team_fixtures.append(game)

    # Only extract the last and next games if there are games arranged for the current season. This is done to
    # prevent errors in the close season when new fixtures may not yet have been added.

    if results and fixtures:
        last_game = team_results[-1]
        next_game = team_fixtures[0]

        return render(request, "team_profile.html", {'team': team, 'items': items, 'board': board,
                                                     'next_game': next_game, 'last_game': last_game,
                                                     'standings': standings, 'conference': conference,
                                                     'products': products, 'archive': archive})

    else:
        return render(request, "team_profile.html", {'team': team, 'items': items, 'products': products,
                                                     'board': board, 'standings': standings, 'archive': archive})
