# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from .models import Team


# Create your views here.
def home_page(request):
    teams = Team.objects.all
    return render(request, "home.html", {'teams': teams})
