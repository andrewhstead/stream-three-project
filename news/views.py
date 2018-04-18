# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404, redirect
from .models import Item, Comment
from .forms import BlogPostForm, CommentForm
from teams.models import Team
from users.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.template.context_processors import csrf
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.models import Group


# Create your views here.
def news_index(request):
    # Remove blog posts from the news view, as they will be displayed separately.
    all_items = Item.objects.exclude(category_id=6).order_by('-created_date')

    page_items = Paginator(all_items, 20)

    page = request.GET.get('page')

    if page:
        current_page = int(page)
    else:
        current_page = 1

    page_count = page_items.num_pages

    try:
        items = page_items.page(page)
    except EmptyPage:
        items = page_items.page(page_count)
    except PageNotAnInteger:
        items = page_items.page(1)

    return render(request, "news.html", {"items": items, "current_page": current_page,
                                         "page_count": page_count})


def news_item(request, news_id):
    item = get_object_or_404(Item, pk=news_id)
    item.views += 1
    item.save()
    return render(request, "news_item.html", {"item": item})


def news_team(request, team_name):
    team = get_object_or_404(Team, geographic_name=team_name.capitalize())
    all_items = Item.objects.filter(teams=team.id).order_by('-created_date')

    page_items = Paginator(all_items, 20)

    page = request.GET.get('page')

    if page:
        current_page = int(page)
    else:
        current_page = 1

    page_count = page_items.num_pages

    try:
        items = page_items.page(page)
    except EmptyPage:
        items = page_items.page(page_count)
    except PageNotAnInteger:
        items = page_items.page(1)

    return render(request, "news_team.html", {'team': team, 'items': items,
                                              'current_page': current_page})


def blog_home(request):
    posts = Item.objects.filter(category_id=6).order_by('-created_date')

    blogger = Group.objects.get(name='Blogger')
    bloggers = []

    users = User.objects.all()
    for user in users:
        if blogger in user.groups.all():
            bloggers.append(user)

    return render(request, "blogs.html", {'posts': posts, 'bloggers': bloggers})


def blog_index(request, author_name):
    author = User.objects.get(username__iexact=author_name)
    all_posts = Item.objects.filter(author=author).order_by('created_date')

    blogger = Group.objects.get(name='Blogger')
    bloggers = []

    users = User.objects.all()
    for user in users:
        if blogger in user.groups.all():
            bloggers.append(user)

    posts_for = Paginator(all_posts, 10)

    page = request.GET.get('page')
    try:
        posts = posts_for.page(page)
    except EmptyPage:
        posts = posts_for.page(1)
    except PageNotAnInteger:
        posts = posts_for.page(posts_for.num_pages)

    return render(request, "blog_index.html", {'all_posts': all_posts, 'posts': posts,
                                               'author': author, 'bloggers': bloggers})


def blog_post(request, post_id):
    item = Item.objects.get(pk=post_id)
    posts = Item.objects.filter(author=item.author).order_by('-created_date')
    item.views += 1
    item.save()

    blogger = Group.objects.get(name='Blogger')
    bloggers = []

    users = User.objects.all()
    for user in users:
        if blogger in user.groups.all():
            bloggers.append(user)

    return render(request, "blog_post.html", {'item': item, 'posts': posts, 'bloggers': bloggers})


@login_required(login_url='/login/')
def new_blog_post(request):
    user = request.user

    if request.method == 'POST':
        form = BlogPostForm(request.POST)
        if form.is_valid():
            new_post = form.save(False)
            new_post.author = user
            new_post.category_id = 6
            new_post.save()
            messages.success(request, "Your blog post has been added!")

            return redirect(reverse('blog_post', args={new_post.pk}))

    else:
        form = BlogPostForm()

    blogger = Group.objects.get(name='Blogger')
    bloggers = []

    users = User.objects.all()
    for user in users:
        if blogger in user.groups.all():
            bloggers.append(user)

    args = {
        'form': form,
        'form_action': reverse('new_blog_post'),
        'button_text': 'Submit Post',
        'bloggers': bloggers
    }
    args.update(csrf(request))
    return render(request, 'blog_post_form.html', args)


@login_required(login_url='/login/')
def edit_blog(request, post_id):
    post = get_object_or_404(Item, pk=post_id)

    if request.method == 'POST':
        form = BlogPostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save()
            messages.success(request, "Your blog post has been edited.")

            return redirect(reverse('blog_post', args={post.pk}))

    else:
        form = BlogPostForm(instance=post)

    blogger = Group.objects.get(name='Blogger')
    bloggers = []

    users = User.objects.all()
    for user in users:
        if blogger in user.groups.all():
            bloggers.append(user)

    args = {
        'form': form,
        'form_action': reverse('edit_blog', kwargs={'post_id': post.id}),
        'button_text': 'Submit Post',
        'bloggers': bloggers
    }
    args.update(csrf(request))
    return render(request, 'blog_post_form.html', args)


@login_required(login_url='/login/')
def delete_blog(request, post_id):
    post = get_object_or_404(Item, pk=post_id)

    post.delete()

    messages.success(request, "Your post has been deleted.")

    return redirect(reverse('blog_home'))


@login_required(login_url='/login/')
def new_comment(request, item_id):
    item = get_object_or_404(Item, pk=item_id)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(False)
            comment.user = request.user
            comment.item = item
            comment.save()
            messages.success(request, "Your comment has been added!")

            if item.category.name == 'Blog Posts':
                return redirect(reverse('blog_post', args={item.pk}))
            else:
                return redirect(reverse('news', args={item.pk}))

    else:
        form = CommentForm()

    blogger = Group.objects.get(name='Blogger')
    bloggers = []

    users = User.objects.all()
    for user in users:
        if blogger in user.groups.all():
            bloggers.append(user)

    args = {
        'form': form,
        'form_action': reverse('new_comment', args={item.id}),
        'button_text': 'Post Comment',
        'bloggers': bloggers
    }
    args.update(csrf(request))
    return render(request, 'comment_form.html', args)


@login_required(login_url='/login/')
def edit_comment(request, item_id, comment_id):
    item = get_object_or_404(Item, pk=item_id)
    comment = get_object_or_404(Comment, pk=comment_id)

    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            messages.success(request, "Your comment has been successfully edited.")

            if item.category.name == 'Blog Posts':
                return redirect(reverse('blog_post', args={item.pk}))
            else:
                return redirect(reverse('news', args={item.pk}))

    else:
        form = CommentForm(instance=comment)

    blogger = Group.objects.get(name='Blogger')
    bloggers = []

    users = User.objects.all()
    for user in users:
        if blogger in user.groups.all():
            bloggers.append(user)

    args = {
        'form': form,
        'form_action': reverse('edit_comment', kwargs={'item_id': item.id, 'comment_id': comment.id}),
        'button_text': 'Edit Comment',
        'bloggers': bloggers,
        'comment': comment
    }
    args.update(csrf(request))
    return render(request, 'comment_form.html', args)


@login_required(login_url='/login/')
def delete_comment(request, item_id, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    item = get_object_or_404(Item, pk=item_id)

    comment.delete()
    messages.success(request, "Your comment was deleted.")

    return redirect(reverse('news', args={item.pk}))

