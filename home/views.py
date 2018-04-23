# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from games.models import get_standings, Game
from teams.models import Team, Conference
from news.models import Item
from datetime import datetime


# Create your views here.
def home_page(request):

    user = request.user
    news_headlines = Item.objects.exclude(category_id=6).order_by('-created_date')[:7]

    if user.is_authenticated:
        favourite_team = user.favourite_team
        if favourite_team:
            extra_news = Item.objects.filter(teams=favourite_team.id).order_by('-created_date')[:5]

            return render(request, "home.html", {"news_headlines": news_headlines, "favourite_team": favourite_team,
                                                 "extra_news": extra_news})
        else:
            extra_news = Item.objects.exclude(category_id=6).order_by('-created_date')[7:12]

            return render(request, "home.html", {"news_headlines": news_headlines, "extra_news": extra_news})

    else:
        extra_news = Item.objects.exclude(category_id=6).order_by('-created_date')[7:12]

        return render(request, "home.html", {"news_headlines": news_headlines, "extra_news": extra_news})
