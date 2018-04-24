# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from teams.models import Team
from users.models import User

# Available types of products, needed when products are created in the admin area.
TYPE_OPTIONS = (
    ('Cap', "Cap"),
    ('Jersey', "Jersey"),
)

# Size options, needed when each individual item is created in the admin area.
SIZE_OPTIONS = (
    ('XS', "XS"),
    ('S', "S"),
    ('M', "M"),
    ('L', "L"),
    ('XL', "XL"),
    ('XXL', "XXL"),
)

# The status of a user's order. 'Pending' is default before the order is submitted, before changing to 'Received'.
STATUS_OPTIONS = (
    ('Pending', 'Pending'),
    ('Received', 'Received'),
    ('Dispatched', 'Dispatched'),
)


# Create your models here.
# An individual product within the store.
class Product(models.Model):
    type = models.CharField(max_length=25, choices=TYPE_OPTIONS)
    team = models.ForeignKey(Team, related_name='products')
    description = models.CharField(max_length=200)
    picture = models.ImageField(upload_to="images/store/", blank=True, null=True)
    price = models.DecimalField(default=0.00, max_digits=10, decimal_places=2)

    def __unicode__(self):
        return unicode(self.team) + ' ' + unicode(self.description)


# Different items which are available for each product, i.e. one for each size which is being sold.
class Item(models.Model):
    product = models.ForeignKey(Product, related_name='items')
    size = models.CharField(max_length=5, choices=SIZE_OPTIONS)
    stock = models.IntegerField(default=1000)

    def __unicode__(self):
        return unicode(self.product) + ' (' + unicode(self.size) + ')'


# A user's shopping cart, used to store items before purchase and track orders after purchase.
class Cart(models.Model):
    user = models.ForeignKey(User, related_name='cart')
    status = models.CharField(max_length=20, default='Pending', choices=STATUS_OPTIONS)
    cost = models.DecimalField(default=0.00, max_digits=10, decimal_places=2)
    postage = models.DecimalField(default=0.00, max_digits=10, decimal_places=2)
    total = models.DecimalField(default=0.00, max_digits=10, decimal_places=2)
    date = models.DateTimeField(blank=True, null=True)
    stripe_id = models.CharField(max_length=40, default='')
    delivery_name = models.CharField(max_length=50, blank=True, null=True)
    address_line_1 = models.CharField(max_length=100, blank=True, null=True)
    address_line_2 = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    postcode = models.CharField(max_length=10, blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True)

    def __unicode__(self):
        return unicode(self.user) + ' (' + unicode(self.id) + ')'


# Each item that the user has in their cart. Quantity of each must be tracked even while orders are pending in order
# to preserve accurate stock records.
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items')
    item = models.ForeignKey(Item, related_name='items')
    quantity = models.IntegerField(default=0)

    def __unicode__(self):
        return unicode(self.cart) + ' (' + unicode(self.id) + ')'
