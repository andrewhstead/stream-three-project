# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from home.views import home_page
from django.core.urlresolvers import resolve


class HomePageTest(TestCase):
    def test_home_page_resolves(self):
        site_home = resolve('/')
        self.assertEqual(site_home.func, home_page)
