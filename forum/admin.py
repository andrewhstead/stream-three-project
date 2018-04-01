# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Section, Board, Thread, Post


# Register your models here.
admin.site.register(Section)
admin.site.register(Board)
admin.site.register(Thread)
admin.site.register(Post)
