# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Message, Sponsor

# Register your models here.
admin.site.register(Message)
admin.site.register(Sponsor)
