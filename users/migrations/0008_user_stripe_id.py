# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-04-06 15:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_auto_20180406_1349'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='stripe_id',
            field=models.CharField(default='', max_length=40),
        ),
    ]