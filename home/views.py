# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from teams.models import Team
from news.models import Item


# Create your views here.
def home_page(request):

    news = Item.objects.exclude(category_id=6).order_by('-created_date')

    return render(request, "home.html", {'news': news})
