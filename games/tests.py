# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.test import TestCase
from .views import last_and_next, league_standings, games_team, results_list, fixture_list,\
    full_results, full_fixtures, season_archive, season_overview, season_team
from django.core.urlresolvers import resolve


class LastNextTest(TestCase):
    def test_last_and_next_resolves(self):
        results_latest = resolve('/scores/')
        self.assertEqual(results_latest.func, last_and_next)


class LeagueStandingsTest(TestCase):
    def test_league_standings_resolves(self):
        standings = resolve('/standings/')
        self.assertEqual(standings.func, league_standings)


class GamesTeamTest(TestCase):
    def test_games_team_resolves(self):
        scores_team = resolve('/scores/london/')
        self.assertEqual(scores_team.func, games_team)


class FullResultsTest(TestCase):
    def test_full_results_resolves(self):
        more_results = resolve('/scores/results/')
        self.assertEqual(more_results.func, full_results)


class FullFixturesTest(TestCase):
    def test_full_fixtures_resolves(self):
        more_fixtures = resolve('/scores/fixtures/')
        self.assertEqual(more_fixtures.func, full_fixtures)


class ResultsListTest(TestCase):
    def test_results_list_resolves(self):
        all_results = resolve('/scores/results/all/')
        self.assertEqual(all_results.func, results_list)


class FixtureListTest(TestCase):
    def test_fixture_list_resolves(self):
        all_fixtures = resolve('/scores/fixtures/all/')
        self.assertEqual(all_fixtures.func, fixture_list)


class SeasonArchiveTest(TestCase):
    def test_season_archive_resolves(self):
        archive_index = resolve('/archive/')
        self.assertEqual(archive_index.func, season_archive)


class SeasonOverviewTest(TestCase):
    def test_season_overview_resolves(self):
        past_season = resolve('/archive/2008/')
        self.assertEqual(past_season.func, season_overview)


class SeasonTeamTest(TestCase):
    def test_season_team_resolves(self):
        team_season = resolve('/archive/2011/cardiff/')
        self.assertEqual(team_season.func, season_team)
