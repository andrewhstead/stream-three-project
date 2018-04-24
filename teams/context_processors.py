from .models import Team, League


# Makes an alphabetical list of teams available to every page on the site -
# required in order to display the team# logos at the top of each page.
def team_list(request):
    return {'teams': Team.objects.all().order_by('geographic_name')}


# Makes the league object available in every page.
def league(request):
    return {'league': League.objects.get(pk=1)}
