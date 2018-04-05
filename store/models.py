# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from teams.models import Team
from users.models import User

TYPE_OPTIONS = (
    ('Cap', "Cap"),
    ('Jersey', "Jersey"),
    ('Hoodie', "Hoodie"),
)

SIZE_OPTIONS = (
    ('XS', "XS"),
    ('S', "S"),
    ('M', "M"),
    ('L', "L"),
    ('XL', "XL"),
    ('XXL', "XXL"),
)

STATUS_OPTIONS = (
    ('Pending', 'Pending'),
    ('Received', 'Received'),
    ('Dispatched', 'Dispatched'),
)


# Create your models here.
class Product(models.Model):
    type = models.CharField(max_length=25, choices=TYPE_OPTIONS)
    team = models.ForeignKey(Team, related_name='products')
    description = models.CharField(max_length=200)
    picture = models.ImageField(upload_to="images/store/", blank=True, null=True)
    price = models.DecimalField(default=0.00, max_digits=10, decimal_places=2)

    def __unicode__(self):
        return unicode(self.team) + ' ' + unicode(self.description)


class Item(models.Model):
    product = models.ForeignKey(Product, related_name='items')
    size = models.CharField(max_length=5, choices=SIZE_OPTIONS)
    stock = models.IntegerField(default=1000)

    def __unicode__(self):
        return unicode(self.product) + ' (' + unicode(self.size) + ')'


class Cart(models.Model):
    user = models.ForeignKey(User, related_name='cart')
    status = models.CharField(max_length=20, default='Pending', choices=STATUS_OPTIONS)
    cost = models.DecimalField(default=0.00, max_digits=10, decimal_places=2)
    stripe_id = models.CharField(max_length=40, default='')

    def __unicode__(self):
        return unicode(self.user) + ' (' + unicode(self.id) + ')'


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items')
    item = models.ForeignKey(Item, related_name='items')
    quantity = models.IntegerField(default=0)

    def __unicode__(self):
        return unicode(self.cart) + ' (' + unicode(self.id) + ')'
