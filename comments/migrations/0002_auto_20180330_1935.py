# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-03-30 18:35
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comments',
            old_name='article',
            new_name='item',
        ),
    ]
