# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from .models import Game
from teams.models import Team
from datetime import date, timedelta


# Create your views here.
def game_index(request):

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
