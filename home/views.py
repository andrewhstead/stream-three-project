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
    news_headlines = Item.objects.exclude(category_id=6).order_by('-created_date')[:5]
    older_news = Item.objects.exclude(category_id=6).order_by('-created_date')[5:10]
    standings = get_standings(current_season)

    return render(request, "home.html", {'news_headlines': news_headlines, 'older_news': older_news,
                                         'teams': teams, 'conferences': conferences, 'standings': standings})
