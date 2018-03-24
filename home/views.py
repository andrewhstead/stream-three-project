# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from teams.models import Team


# Create your views here.
def home_page(request):
    return render(request, "home.html")
