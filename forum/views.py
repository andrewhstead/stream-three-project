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
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.utils import timezone


# Create your views here.
# Show the list of boards in the forum, divided into sections.
# The ten most recent posts are included in the sidebar on forum pages.
def forum_home(request):
    sections = Section.objects.all()
    boards = Board.objects.all()
    recent_posts = Post.objects.all().order_by('-created_date')[:10]

    return render(request, 'forum.html', {'sections': sections, 'boards': boards, 'recent_posts': recent_posts})


# A forum specific to an individual team. The team name is needed along with all the threads on the board.
def forum_team(request, team_name):
    team = get_object_or_404(Team, geographic_name=team_name.capitalize())
    board = Board.objects.get(team=team)
    all_threads = board.threads.all().order_by('-last_post')
    recent_posts = Post.objects.all().order_by('-created_date')[:10]

    # Pagination is used to show only ten threads at a time.
    page_threads = Paginator(all_threads, 10)

    page = request.GET.get('page')

    try:
        threads = page_threads.page(page)
    except EmptyPage:
        threads = page_threads.page(page_threads.num_pages)
    except PageNotAnInteger:
        threads = page_threads.page(1)

    return render(request, 'board.html', {'board': board, 'team': team,
                                          'threads': threads, 'recent_posts': recent_posts})


# A league-wide board, which is identified by its primary key.
def forum_league(request, board_id):
    board = Board.objects.get(pk=board_id)
    all_threads = board.threads.all().order_by('-last_post')
    recent_posts = Post.objects.all().order_by('-created_date')[:10]

    # Only ten threads are shown at a time using pagination.
    page_threads = Paginator(all_threads, 10)

    page = request.GET.get('page')

    try:
        threads = page_threads.page(page)
    except EmptyPage:
        threads = page_threads.page(page_threads.num_pages)
    except PageNotAnInteger:
        threads = page_threads.page(1)

    return render(request, 'board.html', {'board': board, 'board_id': board_id,
                                          'threads': threads, 'recent_posts': recent_posts})


# Create a new thread, using both the new thread form and the new post form to create the first post.
@login_required(login_url='/login/')
def new_thread(request, board_id):
    board = get_object_or_404(Board, pk=board_id)
    recent_posts = Post.objects.all().order_by('-created_date')[:10]

    if request.method == 'POST':
        thread_form = ThreadForm(request.POST)
        post_form = PostForm(request.POST)
        if thread_form.is_valid() and post_form.is_valid():
            # Before saving the thread, allocate it to the user and to the selected board and increment the post count.
            thread = thread_form.save(False)
            thread.user = request.user
            thread.board = board
            thread.post_count += 1
            thread.save()
            # Increment the thread and post count for the relevant board.
            board.post_count += 1
            board.thread_count += 1
            board.save()

            # Before saving the post, allocate it to the user and to the new thread.
            post = post_form.save(False)
            post.user = request.user
            post.thread = thread
            post.board = board
            post.save()

            if board.team_id:
                team = Team.objects.get(pk=board.team_id)
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


# Show the user an individual thread.
def view_thread(request, thread_id):
    thread = get_object_or_404(Thread, pk=thread_id)
    board = Board.objects.get(pk=thread.board_id)
    recent_posts = Post.objects.all().order_by('-created_date')[:10]

    # URL used to ensure thread.views is only incremented once if a user browses a paginated thread.
    # Otherwise a view would be counted for each page in the thread.
    url = request.get_full_path()
    if url == "/thread/" + unicode(thread.id) + '/':
        thread.views += 1
        thread.save()

    # Pagination shows ten threads at a time.
    all_posts = thread.posts.all().order_by('created_date')

    posts_per_page = 10
    page_posts = Paginator(all_posts, posts_per_page)
    pages = page_posts.num_pages

    page = request.GET.get('page')

    # Calculation of the number of posts before the currently viewed page. This is done to ensure the correct number
    # appears in the post count, i.e. with 10 posts per page, the first post on page 2 should be Post 11.
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
                                               'recent_posts': recent_posts, 'pages': pages})

    else:
        return render(request, 'thread.html', {'thread': thread, 'board': board, 'posts': posts, 'pages': pages,
                                               'page': page, 'previous': previous, 'recent_posts': recent_posts})


# Add a new post to an existing thread, or create the first post in a new thread.
@login_required(login_url='/login/')
def new_post(request, thread_id):
    thread = get_object_or_404(Thread, pk=thread_id)
    recent_posts = Post.objects.all().order_by('-created_date')[:10]

    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():

            # Don't save the post until it has been allocated to the user and to the relevant thread.
            post = form.save(False)
            post.user = request.user
            post.thread = thread
            post.board = thread.board
            post.save()
            # Update the thread's last_post field with the current time, and increment the post count by one.
            thread.last_post = timezone.now()
            thread.post_count += 1
            thread.save()
            post.board.post_count += 1
            post.board.save()

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


# Edit an existing forum post.
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


# Delete a currently existing post.
@login_required(login_url='/login/')
def delete_post(request, thread_id, post_id):
    post = get_object_or_404(Post, pk=post_id)
    thread = get_object_or_404(Thread, pk=thread_id)
    board = post.board

    # When the post is deleted, reduce the thread's post count by one.
    post.delete()
    thread.post_count -= 1

    # If no posts remain, delete the thread, and reduce the relevant board's thread and post counts by one.
    if thread.post_count == 0:
        thread.delete()
        board.thread_count -= 1
        board.post_count -= 1
        board.save()

        messages.success(request, "No posts remaining, thread has been deleted.")
        return redirect(reverse('forum'))

    # If there are posts remaining, recalculate the thread's last_post field to the created_date of the last
    # remaining post. This is done in case the deleted post is the last one, to ensure that the last_post field
    # relates to the last remaining post. Also, reduce the relevant board's post count by one.
    else:
        thread.last_post = thread.posts.last().created_date
        thread.save()
        board.post_count -= 1
        board.save()

        messages.success(request, "Your post has been deleted.")
        return redirect(reverse('view_thread', args={thread.pk}))
