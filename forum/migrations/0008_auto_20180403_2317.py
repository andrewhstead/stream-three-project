# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-04-03 22:17
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0007_thread_last_post'),
    ]

    operations = [
        migrations.AlterField(
            model_name='thread',
            name='last_post',
            field=models.DateTimeField(default=datetime.datetime(2018, 4, 3, 23, 17, 49, 81000)),
        ),
    ]