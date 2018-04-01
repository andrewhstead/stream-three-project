# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from .models import Section, Board, Thread, Post


# Create your views here.
def forum_home(request):
    sections = Section.objects.all()
    boards = Board.objects.all()
    return render(request, 'forum.html', {'sections': sections, 'boards': boards})
