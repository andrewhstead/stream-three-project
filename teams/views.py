# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404
from .models import Team


# Create your views here.
def team_index(request):
    teams = Team.objects.all().order_by('geographic_name')
    return render(request, "index.html", {'teams': teams})


def team_page(request, team_id):
    teams = Team.objects.all().order_by('geographic_name')
    team = get_object_or_404(Team, pk=team_id)
    return render(request, "profile.html", {'teams': teams, 'team': team})
