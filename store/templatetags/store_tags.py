# -*- coding: UTF-8 -*-

from django import template

register = template.Library()


@register.filter
def price_display(price):
    view_price = price / 100
    price_in_pounds = '£' + str(view_price)
    return price_in_pounds
