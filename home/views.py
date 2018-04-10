# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from games.models import get_standings
from teams.models import Team, Conference
from news.models import Item
from datetime import datetime


# Create your views here.
def home_page(request):

    current_season = datetime.now().year

    teams = Team.objects.all()
    conferences = Conference.objects.all()
    news = Item.objects.exclude(category_id=6).order_by('-created_date')[:5]
    standings = get_standings(current_season)

    return render(request, "home.html", {'news': news, 'standings': standings,
                                         'teams': teams, 'conferences': conferences})
