# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-04-10 12:24
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0008_auto_20180409_1809'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='author',
            field=models.ForeignKey(default='1', on_delete=django.db.models.deletion.CASCADE, related_name='news',
                                    to=settings.AUTH_USER_MODEL),
        ),
    ]
