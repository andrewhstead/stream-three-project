# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.test import TestCase
from .views import team_index, team_page
from django.core.urlresolvers import resolve
from django.shortcuts import render_to_response

# Test the team index page.
class TeamIndexTest(TestCase):
    def test_team_index_resolves(self):
        teams_home = resolve('/teams/')
        self.assertEqual(teams_home.func, team_index)

    def test_team_index_code(self):
        teams_home = self.client.get('/teams/')
        self.assertEqual(teams_home.status_code, 200)

    def test_team_index_content(self):
        teams_home = self.client.get('/teams/')
        self.assertTemplateUsed(teams_home, 'teams.html')


# Test the team profile page.
class TeamPageTest(TestCase):

    fixtures = ['teams', 'forum', 'users']

    def test_team_page_resolves(self):
        team_profile = resolve('/teams/glasgow/')
        self.assertEqual(team_profile.func, team_page)

    def test_team_page_code(self):
        team_profile = self.client.get('/teams/glasgow/')
        self.assertEqual(team_profile.status_code, 200)

    def test_team_page_content(self):
        team_profile = self.client.get('/teams/glasgow/')
        self.assertTemplateUsed(team_profile, 'team_profile.html')
