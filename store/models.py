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
    ('Complete', 'Complete'),
)


# Create your models here.
class Product(models.Model):
    type = models.CharField(max_length=25, choices=TYPE_OPTIONS)
    team = models.ForeignKey(Team, related_name='products')
    description = models.CharField(max_length=200)
    picture = models.ImageField(upload_to="images/store/", blank=True, null=True)
    price = models.IntegerField(default=0)

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
    cost = models.IntegerField(default=0)
    items = models.ManyToManyField(Item, related_name='cart')

    def __unicode__(self):
        return unicode(self.user) + ' (' + unicode(self.id) + ')'
