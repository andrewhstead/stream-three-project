# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-04-05 20:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0014_cart_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='stripe_id',
            field=models.CharField(default='', max_length=40),
        ),
    ]