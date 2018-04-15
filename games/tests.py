# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.test import TestCase
from .views import last_and_next, league_standings, games_team, results_list, fixture_list,\
    full_results, full_fixtures, season_archive, season_overview, season_team
from django.core.urlresolvers import resolve
from django.shortcuts import render_to_response
from .models import Game
from teams.models import Team


class LastNextTest(TestCase):

    fixtures = ['games', 'teams']

    def test_last_and_next_resolves(self):
        results_latest = resolve('/scores/')
        self.assertEqual(results_latest.func, last_and_next)

    def test_last_and_next_code(self):
        results_latest = self.client.get('/scores/')
        self.assertEqual(results_latest.status_code, 200)

    # def test_last_and_next_content(self):
    #     results_latest = self.client.get('/scores/')
    #     self.assertTemplateUsed(results_latest, 'games_latest.html')
    #     results_latest_template_output = render_to_response("games_latest.html",
    #                                                         {'games': Game.objects.all(),
    #                                                          'teams': Team.objects.all()}).content
    #     self.assertEqual(results_latest.content, results_latest_template_output)


class LeagueStandingsTest(TestCase):
    def test_league_standings_resolves(self):
        standings = resolve('/standings/')
        self.assertEqual(standings.func, league_standings)

    def test_league_standings_code(self):
        standings = self.client.get('/standings/')
        self.assertEqual(standings.status_code, 200)

    def test_league_standings_content(self):
        standings = self.client.get('/standings/')
        self.assertTemplateUsed(standings, 'season_standings.html')


class GamesTeamTest(TestCase):

    fixtures = ['games', 'teams']

    def test_games_team_resolves(self):
        scores_team = resolve('/scores/london/')
        self.assertEqual(scores_team.func, games_team)

    def test_games_team_code(self):
        scores_team = self.client.get('/scores/london/')
        self.assertEqual(scores_team.status_code, 200)

    def test_games_team_content(self):
        scores_team = self.client.get('/scores/london/')
        self.assertTemplateUsed(scores_team, 'games_team.html')


class FullResultsTest(TestCase):
    def test_full_results_resolves(self):
        more_results = resolve('/scores/results/')
        self.assertEqual(more_results.func, full_results)

    def test_full_results_code(self):
        more_results = self.client.get('/scores/results/')
        self.assertEqual(more_results.status_code, 200)

    def test_full_results_content(self):
        more_results = self.client.get('/scores/results/')
        self.assertTemplateUsed(more_results, 'results_full.html')


class FullFixturesTest(TestCase):
    def test_full_fixtures_resolves(self):
        more_fixtures = resolve('/scores/fixtures/')
        self.assertEqual(more_fixtures.func, full_fixtures)

    def test_full_fixtures_code(self):
        more_fixtures = self.client.get('/scores/fixtures/')
        self.assertEqual(more_fixtures.status_code, 200)

    def test_full_fixtures_content(self):
        more_fixtures = self.client.get('/scores/fixtures/')
        self.assertTemplateUsed(more_fixtures, 'fixtures_full.html')


class ResultsListTest(TestCase):
    def test_results_list_resolves(self):
        all_results = resolve('/scores/results/all/')
        self.assertEqual(all_results.func, results_list)

    def test_results_list_code(self):
        all_results = self.client.get('/scores/results/all/')
        self.assertEqual(all_results.status_code, 200)

    def test_results_list_content(self):
        all_results = self.client.get('/scores/results/all/')
        self.assertTemplateUsed(all_results, 'results_list.html')


class FixtureListTest(TestCase):
    def test_fixture_list_resolves(self):
        all_fixtures = resolve('/scores/fixtures/all/')
        self.assertEqual(all_fixtures.func, fixture_list)

    def test_fixture_list_code(self):
        all_fixtures = self.client.get('/scores/fixtures/all/')
        self.assertEqual(all_fixtures.status_code, 200)

    def test_fixture_list_content(self):
        all_fixtures = self.client.get('/scores/fixtures/all/')
        self.assertTemplateUsed(all_fixtures, 'fixture_list.html')


class SeasonArchiveTest(TestCase):
    def test_season_archive_resolves(self):
        archive_index = resolve('/archive/')
        self.assertEqual(archive_index.func, season_archive)

    def test_season_archive_code(self):
        archive_index = self.client.get('/archive/')
        self.assertEqual(archive_index.status_code, 200)

    def test_season_archive_content(self):
        archive_index = self.client.get('/archive/')
        self.assertTemplateUsed(archive_index, 'season_archive.html')


class SeasonOverviewTest(TestCase):

    fixtures = ['games', 'teams']

    def test_season_overview_resolves(self):
        past_season = resolve('/archive/2008/')
        self.assertEqual(past_season.func, season_overview)

    def test_season_overview_code(self):
        past_season = self.client.get('/archive/2008/')
        self.assertEqual(past_season.status_code, 200)

    def test_season_overview_content(self):
        past_season = self.client.get('/archive/2008/')
        self.assertTemplateUsed(past_season, 'season_overview.html')


class SeasonTeamTest(TestCase):

    fixtures = ['games', 'teams']

    def test_season_team_resolves(self):
        team_season = resolve('/archive/2011/cardiff/')
        self.assertEqual(team_season.func, season_team)

    def test_season_team_code(self):
        team_season = self.client.get('/archive/2011/cardiff/')
        self.assertEqual(team_season.status_code, 200)

    def test_season_team_content(self):
        team_season = self.client.get('/archive/2011/cardiff/')
        self.assertTemplateUsed(team_season, 'season_team.html')
