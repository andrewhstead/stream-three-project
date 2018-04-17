# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from games.models import get_standings, Game
from teams.models import Team, Conference
from news.models import Item
from datetime import datetime


# Create your views here.
def home_page(request):

    news_headlines = Item.objects.exclude(category_id=6).order_by('-created_date')[:7]

    return render(request, "home.html", {"news_headlines": news_headlines})
