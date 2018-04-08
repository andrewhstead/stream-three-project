# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404
from .models import Item
from teams.models import Team
from users.models import User


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
