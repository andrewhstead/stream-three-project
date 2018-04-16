from datetime import datetime
from .models import get_standings, Game
from teams.models import Conference


def statistics_bar(request):

    current_season = datetime.now().year

    conferences = Conference.objects.all()
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

        return {"conferences": conferences, "standings": standings,
                "results": latest_results, "fixtures": next_fixtures,
                "latest_date": latest_date, "next_date": next_date}

    elif results:
        latest_date = results.order_by('-game_date')[0].game_date
        latest_results = Game.objects.filter(game_date=latest_date).order_by('home_team')

        return {"conferences": conferences, "standings": standings,
                "results": latest_results, "latest_date": latest_date}

    elif fixtures:
        next_date = fixtures.order_by('game_date')[0].game_date
        next_fixtures = Game.objects.filter(game_date=next_date).order_by('home_team')

        return {"conferences": conferences, "standings": standings,
                "fixtures": next_fixtures, "next_date": next_date}

    else:
        return {"conferences": conferences, "standings": standings}