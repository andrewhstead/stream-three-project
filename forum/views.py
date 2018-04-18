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
from django.contrib import messages
from django.utils import timezone


# Create your views here.
def forum_home(request):
    sections = Section.objects.all()
    boards = Board.objects.all()
    recent_posts = Post.objects.all().order_by('-created_date')[:10]

    return render(request, 'forum.html', {'sections': sections, 'boards': boards, 'recent_posts': recent_posts})


def forum_team(request, team_name):
    team = get_object_or_404(Team, geographic_name=team_name.capitalize())
    board = get_object_or_404(Board, team=team)
    all_threads = board.threads.all().order_by('-last_post')
    recent_posts = Post.objects.all().order_by('-created_date')[:10]

    page_threads = Paginator(all_threads, 20)

    page = request.GET.get('page')

    try:
        threads = page_threads.page(page)
    except EmptyPage:
        threads = page_threads.page(page_threads.num_pages)
    except PageNotAnInteger:
        threads = page_threads.page(1)

    return render(request, 'board.html', {'board': board, 'team': team, 'threads': threads, 'recent_posts': recent_posts})


def forum_league(request, board_id):
    board = get_object_or_404(Board, pk=board_id)
    all_threads = board.threads.all().order_by('-last_post')
    recent_posts = Post.objects.all().order_by('-created_date')[:10]

    page_threads = Paginator(all_threads, 20)

    page = request.GET.get('page')

    try:
        threads = page_threads.page(page)
    except EmptyPage:
        threads = page_threads.page(page_threads.num_pages)
    except PageNotAnInteger:
        threads = page_threads.page(1)

    return render(request, 'board.html', {'board': board, 'threads': threads, 'recent_posts': recent_posts})


@login_required(login_url='/login/')
def new_thread(request, board_id):
    board = get_object_or_404(Board, pk=board_id)
    recent_posts = Post.objects.all().order_by('-created_date')[:10]

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
                messages.success(request, "Your thread was created!")
                return redirect(reverse('forum_team', args={team.geographic_name}))

            else:
                messages.success(request, "Your thread was created!")
                return redirect(reverse('forum_league', args={board.pk}))

    else:
        thread_form = ThreadForm()
        post_form = PostForm()

    args = {
        'thread_form': thread_form,
        'post_form': post_form,
        'board': board,
        'button_text': 'Start Thread',
        'recent_posts': recent_posts
    }
    args.update(csrf(request))

    return render(request, 'thread_form.html', args)


def view_thread(request, thread_id):
    thread = get_object_or_404(Thread, pk=thread_id)
    board = get_object_or_404(Board, pk=thread.board_id)
    recent_posts = Post.objects.all().order_by('-created_date')[:10]

    # URL used to ensure thread.views is only incremented once if a user browses a paginated thread.
    url = request.get_full_path()
    if url == "/thread/" + unicode(thread.id) + '/':
        thread.views += 1
        thread.save()

    all_posts = thread.posts.all()

    posts_per_page = 20
    page_posts = Paginator(all_posts, posts_per_page)

    page = request.GET.get('page')

    if page:
        page_number = int(page)
    else:
        page_number = 1

    previous = posts_per_page * (page_number - 1)

    try:
        posts = page_posts.page(page)
    except EmptyPage:
        posts = page_posts.page(page_posts.num_pages)
    except PageNotAnInteger:
        posts = page_posts.page(1)

    if board.team_id:
        team = get_object_or_404(Team, pk=board.team_id)
        return render(request, 'thread.html', {'thread': thread, 'board': board, 'team': team,
                                               'posts': posts, 'page': page, 'previous': previous,
                                               'recent_posts': recent_posts})

    else:
        return render(request, 'thread.html', {'thread': thread, 'board': board, 'posts': posts,
                                               'page': page, 'previous': previous, 'recent_posts': recent_posts})


@login_required(login_url='/login/')
def new_post(request, thread_id):
    thread = get_object_or_404(Thread, pk=thread_id)
    recent_posts = Post.objects.all().order_by('-created_date')[:10]

    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():

            post = form.save(False)
            post.user = request.user
            post.thread = thread
            post.save()
            thread.last_post = timezone.now()
            thread.save()

            messages.success(request, "Your post was successful!")

        return redirect(reverse('view_thread', args={thread.pk}))

    else:
        form = PostForm()

    args = {
        'form': form,
        'thread': thread,
        'recent_posts': recent_posts,
        'button_text': 'Submit Post'
    }
    args.update(csrf(request))

    return render(request, 'post_form.html', args)


@login_required(login_url='/login/')
def edit_post(request, thread_id, post_id):
    thread = get_object_or_404(Thread, pk=thread_id)
    post = get_object_or_404(Post, pk=post_id)
    recent_posts = Post.objects.all().order_by('-created_date')[:10]

    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()

        messages.success(request, "Your post has been successfully edited.")

        return redirect(reverse('view_thread', args={thread.pk}))

    else:
        form = PostForm(instance=post)

    args = {
        'form': form,
        'thread': thread,
        'form_action': reverse('edit_post', kwargs={'thread_id': thread.id, 'post_id': post.id}),
        'button_text': 'Edit Post',
        'recent_posts': recent_posts,
        'post': post
    }
    args.update(csrf(request))
    return render(request, 'post_form.html', args)


@login_required(login_url='/login/')
def delete_post(request, thread_id, post_id):
    post = get_object_or_404(Post, pk=post_id)
    thread = get_object_or_404(Thread, pk=thread_id)

    post.delete()
    thread.last_post = thread.posts.last().created_date
    thread.save()

    messages.success(request, "Your post has been deleted.")

    return redirect(reverse('view_thread', args={thread.pk}))
