# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from .views import forum_home, forum_league, forum_team, new_thread, view_thread, new_post, edit_post, delete_post
from django.core.urlresolvers import resolve
from .forms import ThreadForm, PostForm


class ForumHomeTest(TestCase):
    def test_forum_home_resolves(self):
        message_board = resolve('/forum/')
        self.assertEqual(message_board.func, forum_home)


class LeagueForumTest(TestCase):
    def test_league_forum_resolves(self):
        message_board = resolve('/forum/league/1/')
        self.assertEqual(message_board.func, forum_league)


class TeamForumTest(TestCase):
    def test_team_forum_resolves(self):
        message_board = resolve('/forum/birmingham/')
        self.assertEqual(message_board.func, forum_team)


class NewThreadTest(TestCase):
    def test_new_thread_resolves(self):
        thread_start = resolve('/thread/new/1/')
        self.assertEqual(thread_start.func, new_thread)


class ViewThreadTest(TestCase):
    def test_view_thread_resolves(self):
        thread_view = resolve('/thread/1/')
        self.assertEqual(thread_view.func, view_thread)


class NewPostTest(TestCase):
    def test_new_post_resolves(self):
        add_post = resolve('/post/new/1/')
        self.assertEqual(add_post.func, new_post)


class EditPostTest(TestCase):
    def test_edit_post_resolves(self):
        change_post = resolve('/post/edit/1/1/')
        self.assertEqual(change_post.func, edit_post)


class DeletePostTest(TestCase):
    def test_delete_post_resolves(self):
        remove_post = resolve('/post/delete/1/1/')
        self.assertEqual(remove_post.func, delete_post)


class ThreadFormTest(TestCase):
    def test_thread_form(self):
        form = ThreadForm({
            'title': 'Thread Title'
        })
        self.assertTrue(form.is_valid())


class PostFormTest(TestCase):
    def test_post_form(self):
        form = PostForm({
            'content': 'The content of the post.'
        })
        self.assertTrue(form.is_valid())
