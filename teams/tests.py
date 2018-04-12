# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.test import TestCase
from .views import team_index, team_page
from django.core.urlresolvers import resolve
from django.shortcuts import render_to_response


class TeamIndexTest(TestCase):
    def test_team_index_resolves(self):
        teams_home = resolve('/teams/')
        self.assertEqual(teams_home.func, team_index)


class TeamPageTest(TestCase):
    def test_team_page_resolves(self):
        team_profile = resolve('/teams/glasgow/')
        self.assertEqual(team_profile.func, team_page)
