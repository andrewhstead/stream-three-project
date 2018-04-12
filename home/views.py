# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from games.models import get_standings, Game
from teams.models import Team, Conference
from news.models import Item
from datetime import datetime


# Create your views here.
def home_page(request):

    home = True
    current_season = datetime.now().year

    conferences = Conference.objects.all()
    news_headlines = Item.objects.exclude(category_id=6).order_by('-created_date')[:7]
    standings = get_standings(current_season)

    results = Game.objects.filter(game_date__year=current_season)\
        .filter(game_status__in=["Completed", "Suspended", "Postponed"])
    fixtures = Game.objects.filter(game_date__year=current_season)\
        .filter(game_status__in=["Scheduled", "In Progress"])

    # Dates obtained separately depending on whether there are results and/or fixtures
    # This is done to prevent errors when there is no list from which to obtain the first value.
    if results and fixtures:
        latest_date = results.order_by('-game_date')[0].game_date
        latest_results = Game.objects.filter(game_date=latest_date).order_by('home_team')
        next_date = fixtures.order_by('game_date')[0].game_date
        next_fixtures = Game.objects.filter(game_date=next_date).order_by('home_team')

        return render(request, "home.html", {"home": home, "news_headlines": news_headlines,
                                             "conferences": conferences, "standings": standings,
                                             "results": latest_results, "fixtures": next_fixtures,
                                             "latest_date": latest_date, "next_date": next_date})

    elif results:
        latest_date = results.order_by('-game_date')[0].game_date
        latest_results = Game.objects.filter(game_date=latest_date).order_by('home_team')

        return render(request, "home.html", {"home": home, "news_headlines": news_headlines,
                                             "conferences": conferences, "standings": standings,
                                             "results": latest_results, "latest_date": latest_date})

    elif fixtures:
        next_date = fixtures.order_by('game_date')[0].game_date
        next_fixtures = Game.objects.filter(game_date=next_date).order_by('home_team')

        return render(request, "home.html", {"home": home, "news_headlines": news_headlines,
                                             "conferences": conferences, "standings": standings,
                                             "fixtures": next_fixtures, "next_date": next_date})

    else:
        return render(request, "home.html", {"home": home, "news_headlines": news_headlines,
                                             "conferences": conferences, "standings": standings})
