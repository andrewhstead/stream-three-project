# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404
from .models import Section, Board, Thread, Post
from teams.models import Team
from .forms import ThreadForm, PostForm
from django.template.context_processors import csrf
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required


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


@login_required
def new_thread(request, board_id):
    board = get_object_or_404(Board, pk=board_id)

    if request.method == 'POST':
        thread_form = ThreadForm(request.POST)
        post_form = PostForm(request.POST)
        if thread_form.is_valid() and post_form.is_valid():
            thread = thread_form.save(False)
            thread.user = request.user
            thread.board = board
            thread.save()

            post = post_form.save(False)
            post.user = request.user
            post.thread = thread
            post.save()

            if board.team_id:
                team = get_object_or_404(Team, pk=board.team_id)
                return redirect(reverse('forum_team', args={team.geographic_name}))

            else:
                return redirect(reverse('forum_league', args={board.pk}))

    else:
        thread_form = ThreadForm()
        post_form = PostForm()

    args = {
        'thread_form': thread_form,
        'post_form': post_form,
        'board': board,
        'button_text': 'Start Thread'
    }
    args.update(csrf(request))

    return render(request, 'new_thread.html', args)


def view_thread(request, thread_id):
    thread = get_object_or_404(Thread, pk=thread_id)
    board = get_object_or_404(Board, pk=thread.board_id)

    if board.team_id:
        team = get_object_or_404(Team, pk=board.team_id)
        return render(request, 'thread.html', {'thread': thread, 'board': board, 'team': team})

    else:
        return render(request, 'thread.html', {'thread': thread, 'board': board})
