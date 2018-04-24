# -*- coding: UTF-8 -*-

from django import template

register = template.Library()


# Add a £ sign to the prices in the store.
@register.filter
def price_display(price):
    price_in_pounds = '£' + str(price)
    return price_in_pounds
