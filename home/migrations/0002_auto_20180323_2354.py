# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-03-23 23:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='team',
            old_name='geo_name',
            new_name='geographic_name',
        ),
        migrations.AddField(
            model_name='team',
            name='away_uniform',
            field=models.ImageField(blank=True, null=True, upload_to='images/teams/uniforms'),
        ),
        migrations.AddField(
            model_name='team',
            name='home_uniform',
            field=models.ImageField(blank=True, null=True, upload_to='images/teams/uniforms'),
        ),
        migrations.AddField(
            model_name='team',
            name='large_logo',
            field=models.ImageField(blank=True, null=True, upload_to='images/teams/logos'),
        ),
        migrations.AddField(
            model_name='team',
            name='small_logo',
            field=models.ImageField(blank=True, null=True, upload_to='images/teams/logos'),
        ),
    ]
