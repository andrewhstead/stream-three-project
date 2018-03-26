# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-03-26 13:10
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('teams', '0004_auto_20180326_1050'),
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.CharField(max_length=50)),
                ('title', models.CharField(max_length=200)),
                ('cover_image', models.ImageField(blank=True, null=True, upload_to='images/news/covers')),
                ('content', models.TextField()),
                ('content_image', models.ImageField(blank=True, null=True, upload_to='images/news/content')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('published_date', models.DateTimeField(blank=True, null=True)),
                ('category', models.CharField(max_length=20)),
                ('views', models.IntegerField(default=0)),
                ('teams', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='team', to='teams.Team')),
            ],
        ),
    ]