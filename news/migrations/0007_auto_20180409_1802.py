# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-04-09 17:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0006_auto_20180408_1329'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='teams',
            field=models.ManyToManyField(related_name='item', to='teams.Team'),
        ),
    ]
