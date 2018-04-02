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
from datetime import datetime
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# Create your views here.
def forum_home(request):
    sections = Section.objects.all()
    boards = Board.objects.all()
    return render(request, 'forum.html', {'sections': sections, 'boards': boards})


def forum_team(request, team_name):
    team = get_object_or_404(Team, geographic_name=team_name.capitalize())
    board = get_object_or_404(Board, team=team)
    all_threads = board.threads.all().order_by('-last_post')

    page_threads = Paginator(all_threads, 20)

    page = request.GET.get('page')

    try:
        threads = page_threads.page(page)
    except EmptyPage:
        threads = page_threads.page(page_threads.num_pages)
    except PageNotAnInteger:
        threads = page_threads.page(1)

    return render(request, 'board.html', {'board': board, 'team': team, 'threads': threads})


def forum_league(request, board_id):
    board = get_object_or_404(Board, pk=board_id)
    all_threads = board.threads.all().order_by('-last_post')

    page_threads = Paginator(all_threads, 20)

    page = request.GET.get('page')

    try:
        threads = page_threads.page(page)
    except EmptyPage:
        threads = page_threads.page(page_threads.num_pages)
    except PageNotAnInteger:
        threads = page_threads.page(1)

    return render(request, 'board.html', {'board': board, 'threads': threads})


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

    return render(request, 'thread_form.html', args)


def view_thread(request, thread_id):
    thread = get_object_or_404(Thread, pk=thread_id)
    board = get_object_or_404(Board, pk=thread.board_id)

    all_posts = thread.posts.all()

    page_posts = Paginator(all_posts, 20)

    page = request.GET.get('page')

    try:
        posts = page_posts.page(page)
    except EmptyPage:
        posts = page_posts.page(page_posts.num_pages)
    except PageNotAnInteger:
        posts = page_posts.page(1)

    if board.team_id:
        team = get_object_or_404(Team, pk=board.team_id)
        return render(request, 'thread.html', {'thread': thread, 'board': board,
                                               'team': team, 'posts': posts})

    else:
        return render(request, 'thread.html', {'thread': thread, 'board': board,
                                               'posts': posts, 'page': page})


@login_required
def new_post(request, thread_id):
    thread = get_object_or_404(Thread, pk=thread_id)

    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():

            post = form.save(False)
            post.user = request.user
            post.thread = thread
            post.save()
            thread.last_post = datetime.now()
            thread.save()

        return redirect(reverse('view_thread', args={thread.pk}))

    else:
        form = PostForm()

    args = {
        'form': form,
        'thread': thread,
        'button_text': 'Submit Post'
    }
    args.update(csrf(request))

    return render(request, 'post_form.html', args)


@login_required
def edit_post(request, thread_id, post_id):
    thread = get_object_or_404(Thread, pk=thread_id)
    post = get_object_or_404(Post, pk=post_id)

    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()

        return redirect(reverse('view_thread', args={thread.pk}))

    else:
        form = PostForm(instance=post)

    args = {
        'form': form,
        'thread': thread,
        'form_action': reverse('edit_post', kwargs={'thread_id': thread.id, 'post_id': post.id}),
        'button_text': 'Edit Post',
        'post': post
    }
    args.update(csrf(request))
    return render(request, 'post_form.html', args)


@login_required
def delete_post(request, thread_id, post_id):
    post = get_object_or_404(Post, pk=post_id)
    thread = get_object_or_404(Thread, pk=thread_id)

    post.delete()
    thread.last_post = thread.posts.last().created_date
    thread.save()

    return redirect(reverse('view_thread', args={thread.pk}))
