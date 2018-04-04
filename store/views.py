# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from .models import Product, Item


# Create your views here.
def store_front(request):
    products = Product.objects.all()
    items = Item.objects.all()
    return render(request, 'store.html', {'products': products, 'items': items})
