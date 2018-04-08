# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404, redirect
from .models import Item
from .forms import NewBlogPostForm
from teams.models import Team
from users.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.template.context_processors import csrf


# Create your views here.
def news_index(request):
    items = Item.objects.all()
    return render(request, "news.html", {"items": items})


def news_item(request, news_id):
    item = get_object_or_404(Item, pk=news_id)
    item.views += 1
    item.save()
    return render(request, "news_item.html", {"item": item})


def news_team(request, team_name):
    items = Item.objects.all()
    team = get_object_or_404(Team, geographic_name=team_name.capitalize())
    return render(request, "news_team.html", {'team': team, 'items': items})


def blog_index(request):
    posts = Item.objects.filter(category_id=6).order_by('-created_date')
    return render(request, "blogs.html", {'posts': posts})


def blog_home(request, author_name):
    author = User.objects.get(username__iexact=author_name)
    posts = Item.objects.filter(author=author).order_by('-created_date')
    return render(request, "blog_index.html", {'posts': posts, 'author': author})


def blog_post(request, post_id):
    item = Item.objects.get(pk=post_id)
    posts = Item.objects.filter(author=item.author).order_by('-created_date')
    item.views += 1
    item.save()

    return render(request, "blog_post.html", {'item': item, 'posts': posts})


@login_required(login_url='/login/')
def new_blog_post(request):
    user = request.user

    if request.method == 'POST':
        form = NewBlogPostForm(request.POST)
        if form.is_valid():
            new_post = form.save(False)
            new_post.author = request.user
            new_post.category_id = 6
            new_post.save()
            messages.success(request, "Your blog post has been added!")

            return redirect(reverse('blog_post', args={new_post.pk}))

    else:
        form = NewBlogPostForm()

    args = {
        'form': form,
        'form_action': reverse('new_blog_post'),
        'button_text': 'Submit Post'
    }
    args.update(csrf(request))
    return render(request, 'blog_post_form.html', args)
