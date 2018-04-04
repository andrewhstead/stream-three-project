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


# Create your models here.
class Product(models.Model):
    type = models.CharField(max_length=25, choices=TYPE_OPTIONS)
    team = models.ForeignKey(Team, related_name='products')
    description = models.CharField(max_length=100)
    picture = models.ImageField(upload_to="images/store/", blank=True, null=True)
    price = models.DecimalField(default=0.00, decimal_places=2, max_digits=10)

    def __unicode__(self):
        return unicode(self.team) + ' ' + unicode(self.description)


class Order(models.Model):
    user = models.ForeignKey(User, related_name='orders')
    price = models.DecimalField(default=0.00, decimal_places=2, max_digits=10)
    basket = models.ManyToManyField(Product, related_name="products")

    def __unicode__(self):
        return unicode(self.id) + unicode(self.user)
