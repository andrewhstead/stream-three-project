# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404, redirect
from django.core.urlresolvers import reverse
from .models import Game, Season, get_standings
from .forms import SeasonSelectForm
from teams.models import Team, Conference
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from datetime import datetime
from django.template.context_processors import csrf


# Create your views here.
# Show the results from the most recent game date and the fixtures for the next scheduled game date.
def last_and_next(request):

    current_season = datetime.now().year

    # Get the game information for the current season only.
    results = Game.objects.filter(game_date__year=current_season)\
        .filter(game_status__in=["Completed", "Suspended", "Postponed"])
    fixtures = Game.objects.filter(game_date__year=current_season)\
        .filter(game_status__in=["Scheduled", "In Progress"])

    # Dates obtained separately depending on whether there are results and/or fixtures
    # This is done to prevent errors when there is no list from which to obtain the first value.
    # If both results and fixtures are present:
    if results and fixtures:
        latest_date = results.order_by('-game_date')[0].game_date
        latest_results = Game.objects.filter(game_date=latest_date).order_by('home_team')
        next_date = fixtures.order_by('game_date')[0].game_date
        next_fixtures = Game.objects.filter(game_date=next_date).order_by('home_team')

        return render(request, "games_latest.html", {"results": latest_results, "fixtures": next_fixtures,
                                                     "latest_date": latest_date, "next_date": next_date})
    # If results but not fixtures are present:
    elif results:
        latest_date = results.order_by('-game_date')[0].game_date
        latest_results = Game.objects.filter(game_date=latest_date).order_by('home_team')

        return render(request, "games_latest.html", {"results": latest_results, "latest_date": latest_date})

    # If fixtures but not results are present:
    elif fixtures:
        next_date = fixtures.order_by('game_date')[0].game_date
        next_fixtures = Game.objects.filter(game_date=next_date).order_by('home_team')

        return render(request, "games_latest.html", {"fixtures": next_fixtures, "next_date": next_date})


# Show the league standings for the current season.
def league_standings(request):

    conferences = Conference.objects.all()
    teams = Team.objects.all().order_by('geographic_name')

    # If an option has been selected from the drop-down, set that as the currently displayed season.
    if request.method == 'POST':
        form = SeasonSelectForm(request.POST)
        current_season = request.POST.get('season')

    # Otherwise, the currently displayed season will be the current year
    else:
        form = SeasonSelectForm()
        current_season = datetime.now().year

    # Get the standings for the chosen season.
    standings = get_standings(current_season)

    args = {
        "standings": standings,
        "form": form,
        "conferences": conferences,
        "teams": teams
    }

    args.update(csrf(request))

    return render(request, "season_standings.html", args)


# Show a list of result and fixtures for a chosen team in the current year.
def games_team(request, team_name):

    current_season = datetime.now().year

    # Get the games for the current season.
    games = Game.objects.filter(game_date__year=current_season) \
        .filter(game_type='Regular Season').order_by('game_date')
    team = get_object_or_404(Team, geographic_name=team_name.capitalize())
    # Empty list to define the team's schedule.
    team_schedule = []

    # For each game in the season:
    for game in games:
        # If the chosen team was at home, allocate the home team's result to them and set the away team as their
        # opponent.
        if game.home_team == team:
            game.team = game.home_team
            game.opponent = game.away_team
            game.team_runs = game.home_team_runs
            game.opponent_runs = game.away_team_runs
            team_schedule.append(game)
        # If the chosen team was away, allocate the away team's result to them and set the home team as their opponent.
        elif game.away_team == team:
            game.team = game.away_team
            game.opponent = game.home_team
            game.team_runs = game.away_team_runs
            game.opponent_runs = game.home_team_runs
            team_schedule.append(game)

    return render(request, "games_team.html", {"team": team, "team_games": team_schedule})


# Show a full list of results for the current season in a single page.
def results_list(request):

    current_season = datetime.now().year

    # Get the results for the current season. A game is considered to be a result if it is completed, suspended or
    # postponed. For suspended and postponed games, they will no longer be considered results when they are
    # re-arranged and scheduled for another date.
    results = Game.objects.filter(game_date__year=current_season)\
        .filter(game_type='Regular Season')\
        .filter(game_status__in=["Completed", "Suspended", "Postponed"]) \
        .order_by('home_team').order_by('-game_date')

    # Empty list for dates on which there was at least one result. Add dates to this list in order to show the
    # results one date at a time.
    dates = []
    for result in results:
        if result.game_date not in dates:
            dates.append(result.game_date)
            dates.sort(reverse=True)

    return render(request, "results_list.html", {'results': results, 'dates': dates})


# Show a full list of fixtures for the current season in a single page.
def fixture_list(request):

    current_season = datetime.now().year

    # Get the fixtures for the current season. A game is considered to be a fixture if it is scheduled for a future
    # date or time, or it is in progress.
    fixtures = Game.objects.filter(game_date__year=current_season)\
        .filter(game_type='Regular Season')\
        .filter(game_status__in=["Scheduled", "In Progress"]) \
        .order_by('home_team').order_by('game_time').order_by('game_date')

    # Empty list for dates on which there is at least one fixture. Add dates to this list in order to show the
    # fixtures one date at a time.
    dates = []
    for fixture in fixtures:
        if fixture.game_date not in dates:
            dates.append(fixture.game_date)

    return render(request, "fixture_list.html", {'fixtures': fixtures, 'dates': dates})


# Show a list of results for the current season in paginated format.
def full_results(request):

    current_season = datetime.now().year

    # Get the results for the current season. A game is considered to be a result if it is completed, suspended or
    # postponed. For suspended and postponed games, they will no longer be considered results when they are
    # re-arranged and scheduled for another date.
    results = Game.objects.filter(game_date__year=current_season)\
        .filter(game_type='Regular Season')\
        .filter(game_status__in=["Completed", "Suspended", "Postponed"])\
        .order_by('game_date').order_by('home_team')

    # Empty list for dates on which there was at least one result. Add dates to this list in order to show the
    # results one date at a time.
    date_list = []
    for result in results:
        if result.game_date not in date_list:
            date_list.append(result.game_date)
            date_list.sort(reverse=True)

    # Use pagination to show games on three dates at a time.
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


# Show a list of fixtures for the current season in paginated format.
def full_fixtures(request):

    current_season = datetime.now().year

    # Get the fixtures for the current season. A game is considered to be a fixture if it is scheduled for a future
    # date or time, or it is in progress.
    fixtures = Game.objects.filter(game_date__year=current_season)\
        .filter(game_type='Regular Season')\
        .filter(game_status__in=["Scheduled", "In Progress"]) \
        .order_by('home_team').order_by('game_time').order_by('game_date')

    # Empty list for dates on which there is at least one fixture. Add dates to this list in order to show the
    # fixtures one date at a time.
    date_list = []
    for fixture in fixtures:
        if fixture.game_date not in date_list:
            date_list.append(fixture.game_date)
            date_list.sort()

    # Use pagination to show games on three dates at a time.
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


# Show a list of all season in the league's history, with overview information.
def season_archive(request):
    seasons = Season.objects.all().order_by('year')
    standings = get_standings(datetime.now().year)

    return render(request, "season_archive.html", {'seasons': seasons, 'standings': standings})


# Show an overview of an individual season, with the standings for that year and all play-off games for that season
# shown in full detail.
def season_overview(request, year):

    season = Season.objects.get(year=year)
    seasons = Season.objects.all()

    conferences = Conference.objects.all()
    teams = Team.objects.all().order_by('geographic_name')

    # Get the results from the play-offs in the chosen season.
    championship_series = Game.objects.filter(game_date__year=year, game_type='Postseason')

    # Archive settings needed to allow chosen year's standings alongside current standings in sidebar.
    archive_standings = get_standings(year)
    archive = True

    # If the season has a champion set, i.e. if the season is over, show the archive details.
    if season.champion:
        return render(request, "season_overview.html", {'year': year, 'season': season,
                                                        'seasons': seasons, 'archive_standings': archive_standings,
                                                        'conferences': conferences, 'teams': teams,
                                                        'championship_series': championship_series,
                                                        'archive': archive})

    # If it is the current season, i.e. still in progress, redirect to the standings view.
    else:
        return redirect(reverse('standings'))


# Show an overview of an individual team's past season.
def season_team(request, year, team_name):

    season = Season.objects.get(year=year)
    seasons = Season.objects.all()

    # Get the result details for the chosen season only.
    games = Game.objects.filter(game_date__year=year) \
        .filter(game_type__in=['Regular Season', 'Postseason']).order_by('game_date')

    teams = Team.objects.all().order_by('geographic_name')
    team = get_object_or_404(Team, geographic_name=team_name.capitalize())
    conference = team.conference

    # Empty lists for the team's results and for the championship series if the team was involved.
    team_schedule = []
    championship_series = []

    # Archive settings needed to allow chosen year's standings alongside current standings in sidebar.
    archive_standings = get_standings(year)
    archive = True

    # For each game in the season:
    for game in games:
        # If the chosen team was at home, allocate the home team's result to them and set the away team as their
        # opponent.
        if game.home_team == team:
            game.team = game.home_team
            game.opponent = game.away_team
            game.team_runs = game.home_team_runs
            game.opponent_runs = game.away_team_runs
            # If the game was in the play-offs, add it to the championship_series list. Otherwise add it to the
            # schedule.
            if game.game_type == 'Postseason':
                championship_series.append(game)
            else:
                team_schedule.append(game)
        # If the chosen team was away, allocate the away team's result to them and set the home team as their opponent.
        elif game.away_team == team:
            game.team = game.away_team
            game.opponent = game.home_team
            game.team_runs = game.away_team_runs
            game.opponent_runs = game.home_team_runs
            # If the game was in the play-offs, add it to the championship_series list. Otherwise add it to the
            # schedule.
            if game.game_type == 'Postseason':
                championship_series.append(game)
            else:
                team_schedule.append(game)

    # If the season has a champion set, i.e. if the season is over, show the archive details.
    if season.champion:
        return render(request, "season_team.html", {"season": season, "team": team, "teams": teams,
                                                    "seasons": seasons, "team_games": team_schedule,
                                                    "championship_series": championship_series,
                                                    "archive_standings": archive_standings,
                                                    "conference": conference, "archive": archive})

    # If it is the current season, i.e. still in progress, redirect to the team's current season schedule page.
    else:
        return redirect('team_games', team_name=team_name)
