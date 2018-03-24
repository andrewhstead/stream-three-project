from .models import Team


def team_list(request):
    return {'teams': Team.objects.all().order_by('geographic_name')}
