# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404
from .models import Team


# Create your views here.
def team_index(request):
    return render(request, "index.html")


def team_page(request, team_id):
    team = get_object_or_404(Team, pk=team_id)
    return render(request, "profile.html", {'team': team})
