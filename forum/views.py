# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404
from .models import Section, Board, Thread, Post
from teams.models import Team


# Create your views here.
def forum_home(request):
    sections = Section.objects.all()
    boards = Board.objects.all()
    return render(request, 'forum.html', {'sections': sections, 'boards': boards})


def forum_team(request, team_name):
    team = get_object_or_404(Team, geographic_name=team_name.capitalize())
    board = get_object_or_404(Board, team=team)
    return render(request, 'board.html', {'board': board, 'team': team})


def forum_league(request, board_id):
    board = get_object_or_404(Board, pk=board_id)
    return render(request, 'board.html', {'board': board})
