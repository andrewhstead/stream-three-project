from .models import Game
from teams.models import Team


def league_standings(request):
    teams = Team.objects.all().order_by('geographic_name')
    games = Game.objects.filter(game_status="Completed")
    standings = []

    for team in teams:
        team.record = {"name": team.geographic_name, "conference": team.conference,
                       "small_logo": team.small_logo, "played": 0.0, "won": 0.0, "lost": 0.0}
        for game in games:
            if game.home_team == team:
                team.record["played"] += 1
                if game.home_team_runs > game.away_team_runs:
                    team.record["won"] += 1
                if game.home_team_runs < game.away_team_runs:
                    team.record["lost"] += 1
            elif game.away_team == team:
                team.record["played"] += 1
                if game.away_team_runs > game.home_team_runs:
                    team.record["won"] += 1
                if game.away_team_runs < game.home_team_runs:
                    team.record["lost"] += 1
        team.record["pct"] = team.record["won"] / team.record["played"]
        standings.append(team.record)

    return {"standings": standings}
