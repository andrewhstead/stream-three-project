# -*- coding: UTF-8 -*-
from django import forms
from store.models import Item

SIZE_OPTIONS = (
    ('XS', "XS"),
    ('S', "S"),
    ('M', "M"),
    ('L', "L"),
    ('XL', "XL"),
    ('XXL', "XXL"),
)

QUANTITY_OPTIONS = (
    (1, 1),
    (2, 2),
    (3, 3),
    (4, 4),
    (5, 5),
    (6, 6),
    (7, 7),
    (8, 8),
    (9, 9),
    (10, 10),
)


class AddToCartForm(forms.Form):
    size = forms.ChoiceField(choices=SIZE_OPTIONS)
    quantity = forms.ChoiceField(choices=QUANTITY_OPTIONS)


class ChangeQuantityForm(forms.Form):
    quantity = forms.ChoiceField(choices=QUANTITY_OPTIONS, label="New Quantity")


class SubmitOrderForm(forms.Form):
    MONTH_OPTIONS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

    MONTH_CHOICES = list(enumerate(MONTH_OPTIONS, 1))
    YEAR_CHOICES = [(i, i) for i in range(2018, 2030)]

    card_number = forms.CharField(label='Card Number')
    cvv = forms.CharField(label='CVV')
    expiry_month = forms.ChoiceField(choices=MONTH_CHOICES, label='Month')
    expiry_year = forms.ChoiceField(choices=YEAR_CHOICES, label='Year')
    stripe_id = forms.CharField(widget=forms.HiddenInput)


class SubscriptionForm(SubmitOrderForm):
    CYCLE_OPTIONS = (
        ('BIBL_MONTHLY', '£9.99 Every Month'),
        ('BIBL_THREE', '£27.49 Every 3 Months'),
        ('BIBL_SIX', '£49.99 Every 6 Months'),
        ('BIBL_YEARLY', '£89.99 Every 12 Months'),
    )

    billing_cycle = forms.ChoiceField(choices=CYCLE_OPTIONS)

    class Meta:
        fields = ['billing_cycle', 'card_number', 'cvv', 'expiry_month', 'expiry_year', 'stripe_id']
