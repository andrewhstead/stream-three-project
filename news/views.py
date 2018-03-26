# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404
from .models import Item


# Create your views here.
def news_index(request):
    items = Item.objects.all()
    return render(request, "news.html", {"items": items})


def news_item(request, id):
    item = get_object_or_404(Item, pk=id)
    item.views += 1
    item.save()
    return render(request, "news_item.html", {"item": item})
