# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404
from .models import Game, Season, get_standings
from .forms import SeasonSelectForm
from teams.models import Team, Conference
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from datetime import datetime
from django.template.context_processors import csrf


# Create your views here.
def last_and_next(request):

    current_season = datetime.now().year

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

        return render(request, "games_latest.html", {"results": latest_results, "fixtures": next_fixtures,
                                                     "latest_date": latest_date, "next_date": next_date})
    elif results:
        latest_date = results.order_by('-game_date')[0].game_date
        latest_results = Game.objects.filter(game_date=latest_date).order_by('home_team')

        return render(request, "games_latest.html", {"results": latest_results, "latest_date": latest_date})

    elif fixtures:
        next_date = fixtures.order_by('game_date')[0].game_date
        next_fixtures = Game.objects.filter(game_date=next_date).order_by('home_team')

        return render(request, "games_latest.html", {"fixtures": next_fixtures, "next_date": next_date})


def league_standings(request):

    conferences = Conference.objects.all()
    teams = Team.objects.all().order_by('geographic_name')

    if request.method == 'POST':
        form = SeasonSelectForm(request.POST)
        current_season = request.POST.get('season')

    else:
        form = SeasonSelectForm()
        current_season = datetime.now().year

    standings = get_standings(current_season)

    args = {
        "standings": standings,
        "form": form,
        "conferences": conferences,
        "teams": teams
    }

    args.update(csrf(request))

    return render(request, "season_standings.html", args)


def games_team(request, team_name):

    current_season = datetime.now().year

    games = Game.objects.filter(game_date__year=current_season) \
        .filter(game_type='Regular Season').order_by('game_date')
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


def results_list(request):

    current_season = datetime.now().year

    results = Game.objects.filter(game_date__year=current_season)\
        .filter(game_type='Regular Season')\
        .filter(game_status__in=["Completed", "Suspended", "Postponed"]) \
        .order_by('home_team').order_by('-game_date')
    dates = []

    for result in results:
        if result.game_date not in dates:
            dates.append(result.game_date)
            dates.sort(reverse=True)

    return render(request, "results_list.html", {'results': results, 'dates': dates})


def fixture_list(request):

    current_season = datetime.now().year

    fixtures = Game.objects.filter(game_date__year=current_season)\
        .filter(game_type='Regular Season')\
        .filter(game_status__in=["Scheduled", "In Progress"]) \
        .order_by('home_team').order_by('game_time').order_by('game_date')
    dates = []

    for fixture in fixtures:
        if fixture.game_date not in dates:
            dates.append(fixture.game_date)

    return render(request, "fixture_list.html", {'fixtures': fixtures, 'dates': dates})


def full_results(request):

    current_season = datetime.now().year

    results = Game.objects.filter(game_date__year=current_season)\
        .filter(game_type='Regular Season')\
        .filter(game_status__in=["Completed", "Suspended", "Postponed"])\
        .order_by('game_date').order_by('home_team')
    date_list = []

    for result in results:
        if result.game_date not in date_list:
            date_list.append(result.game_date)
            date_list.sort(reverse=True)

    page_dates = Paginator(date_list, 3)

    page = request.GET.get('page')
    try:
        dates = page_dates.page(page)
    except EmptyPage:
        dates = page_dates.page(page_dates.num_pages)
    except PageNotAnInteger:
        dates = page_dates.page(1)

    return render(request, "results_full.html",
                  {'results': results, 'dates': dates, 'date_list': date_list})


def full_fixtures(request):

    current_season = datetime.now().year

    fixtures = Game.objects.filter(game_date__year=current_season)\
        .filter(game_type='Regular Season')\
        .filter(game_status__in=["Scheduled", "In Progress"]) \
        .order_by('home_team').order_by('game_time').order_by('game_date')
    date_list = []

    for fixture in fixtures:
        if fixture.game_date not in date_list:
            date_list.append(fixture.game_date)
            date_list.sort()

    page_dates = Paginator(date_list, 3)

    page = request.GET.get('page')
    try:
        dates = page_dates.page(page)
    except EmptyPage:
        dates = page_dates.page(page_dates.num_pages)
    except PageNotAnInteger:
        dates = page_dates.page(1)

    return render(request, "fixtures_full.html",
                  {'fixtures': fixtures, 'dates': dates, 'date_list': date_list})


def season_archive(request):
    seasons = Season.objects.all().order_by('year')

    return render(request, "season_archive.html", {'seasons': seasons})


def season_overview(request, year):
    season = Season.objects.get(year=year)

    conferences = Conference.objects.all()
    teams = Team.objects.all().order_by('geographic_name')

    championship_series = Game.objects.filter(game_date__year=year, game_type='Postseason')

    standings = get_standings(year)

    return render(request, "season_overview.html", {'year': year, 'season': season, 'standings': standings,
                                                    'conferences': conferences, 'teams': teams,
                                                    'championship_series': championship_series})
