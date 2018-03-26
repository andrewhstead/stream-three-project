# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404
from .models import Item
from teams.models import Team


# Create your views here.
def news_index(request):
    items = Item.objects.all()
    return render(request, "news.html", {"items": items})


def news_item(request, id):
    item = get_object_or_404(Item, pk=id)
    item.views += 1
    item.save()
    return render(request, "news_item.html", {"item": item})


def news_team(request, team_name):
    items = Item.objects.all()
    team = get_object_or_404(Team, geographic_name=team_name.capitalize())
    return render(request, "news_team.html", {'team': team, 'items': items})
