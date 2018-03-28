# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404
from .models import Game
from teams.models import Team, Conference
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# Create your views here.
def last_and_next(request):

    game_results = Game.objects.filter(game_status__in=["Completed", "Suspended", "Postponed"]).order_by('game_date')
    result_dates = []

    for result in game_results:
        if result.game_date not in result_dates:
            result_dates.append(result.game_date)

    latest_date = result_dates[-1]
    latest_results = game_results.filter(game_date=latest_date).order_by('home_team')

    game_fixtures = Game.objects.filter(game_status__in=["Scheduled", "In Progress"])\
        .order_by('game_date').order_by('home_team')
    fixture_dates = []

    for fixture in game_fixtures:
        if fixture.game_date not in fixture_dates:
            fixture_dates.append(fixture.game_date)

    next_date = fixture_dates[0]
    next_fixtures = game_fixtures.filter(game_date=next_date).order_by('home_team')

    return render(request, "games_latest.html", {"results": latest_results, "fixtures": next_fixtures,
                                                 "latest_date": latest_date, "next_date": next_date})


def league_standings(request):
    conferences = Conference.objects.all()

    return render(request, "standings.html", {"conferences": conferences})


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


def results_list(request):
    results = Game.objects.filter(game_status__in=["Completed", "Suspended", "Postponed"])\
        .order_by('-game_date').order_by('home_team')
    dates = []

    for result in results:
        if result.game_date not in dates:
            dates.append(result.game_date)

    return render(request, "results_list.html", {'results': results, 'dates': dates})


def fixture_list(request):
    fixtures = Game.objects.filter(game_status__in=["Scheduled", "In Progress"])\
        .order_by('game_date').order_by('home_team')
    dates = []

    for fixture in fixtures:
        if fixture.game_date not in dates:
            dates.append(fixture.game_date)

    return render(request, "fixture_list.html", {'fixtures': fixtures, 'dates': dates})


def full_results(request):
    results = Game.objects.filter(game_status__in=["Completed", "Suspended", "Postponed"])\
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
    fixtures = Game.objects.filter(game_status__in=["Scheduled", "In Progress"])\
        .order_by('game_date').order_by('home_team')
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
