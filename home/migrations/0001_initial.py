# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-03-23 23:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('geo_name', models.CharField(max_length=100)),
                ('nickname', models.CharField(max_length=100)),
                ('abbreviation', models.CharField(max_length=5)),
                ('conference', models.CharField(max_length=25)),
                ('ballpark', models.CharField(max_length=100)),
            ],
        ),
    ]
