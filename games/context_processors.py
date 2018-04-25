from datetime import datetime
from .models import get_standings, Game
from teams.models import Conference


# Get the data for the statistics sidebar which is used on the majority of pages through the site. It should show the
#  most recent game results if there are any, the next scheduled fixtures if there are any, and the current league
# standings.
def statistics_bar(request):

    current_season = datetime.now().year

    conferences = Conference.objects.all()
    standings = get_standings(current_season)

    # Get the results for the current year only.
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

        return {"conferences": conferences, "standings": standings,
                "results": latest_results, "fixtures": next_fixtures,
                "latest_date": latest_date, "next_date": next_date}

    # If only results, but no fixtures:
    elif results:
        latest_date = results.order_by('-game_date')[0].game_date
        latest_results = Game.objects.filter(game_date=latest_date).order_by('home_team')

        return {"conferences": conferences, "standings": standings,
                "results": latest_results, "latest_date": latest_date}

    # If only fixtures, but no results:
    elif fixtures:
        next_date = fixtures.order_by('game_date')[0].game_date
        next_fixtures = Game.objects.filter(game_date=next_date).order_by('home_team')

        return {"conferences": conferences, "standings": standings,
                "fixtures": next_fixtures, "next_date": next_date}

    # If neither results nor fixtures are available:
    else:
        return {"conferences": conferences, "standings": standings}