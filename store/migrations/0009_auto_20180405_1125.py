# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-04-05 10:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0008_auto_20180405_1113'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='cost',
            field=models.FloatField(default=0.0),
        ),
    ]
