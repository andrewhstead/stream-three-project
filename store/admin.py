# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Product, Item, Cart, CartItem

# Register your models here.
admin.site.register(Product)
admin.site.register(Item)
admin.site.register(Cart)
admin.site.register(CartItem)
