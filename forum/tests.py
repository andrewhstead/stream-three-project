# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from .views import forum_home, forum_league, forum_team, new_thread, view_thread, new_post, edit_post, delete_post
from django.core.urlresolvers import resolve
from .forms import ThreadForm, PostForm


# Test the home page of the forum.
class ForumHomeTest(TestCase):

    fixtures = ['teams']

    def test_forum_home_resolves(self):
        message_board = resolve('/forum/')
        self.assertEqual(message_board.func, forum_home)

    def test_forum_home_code(self):
        message_board = self.client.get('/forum/')
        self.assertEqual(message_board.status_code, 200)

    def test_forum_home_content(self):
        message_board = self.client.get('/forum/')
        self.assertTemplateUsed(message_board, 'forum.html')


# Test a general league message board.
class LeagueForumTest(TestCase):
    def test_league_forum_resolves(self):
        message_board = resolve('/forum/league/1/')
        self.assertEqual(message_board.func, forum_league)


# Test a team-specific message board.
class TeamForumTest(TestCase):
    def test_team_forum_resolves(self):
        message_board = resolve('/forum/birmingham/')
        self.assertEqual(message_board.func, forum_team)


# Test the view which shows the user a single thread.
class ViewThreadTest(TestCase):
    def test_view_thread_resolves(self):
        thread_view = resolve('/thread/1/')
        self.assertEqual(thread_view.func, view_thread)


# Test the view which allows a new thread to be created.
class NewThreadTest(TestCase):
    def test_new_thread_resolves(self):
        thread_start = resolve('/thread/new/1/')
        self.assertEqual(thread_start.func, new_thread)


# Test the view for creating a new post in a thread.
class NewPostTest(TestCase):
    def test_new_post_resolves(self):
        add_post = resolve('/post/new/1/')
        self.assertEqual(add_post.func, new_post)


# Test the view for editing a forum post.
class EditPostTest(TestCase):
    def test_edit_post_resolves(self):
        change_post = resolve('/post/edit/1/1/')
        self.assertEqual(change_post.func, edit_post)


# Test the view for deleting a post.
class DeletePostTest(TestCase):
    def test_delete_post_resolves(self):
        remove_post = resolve('/post/delete/1/1/')
        self.assertEqual(remove_post.func, delete_post)


# Test the form which creates a new thread.
class ThreadFormTest(TestCase):
    def test_thread_form(self):
        form = ThreadForm({
            'title': 'Thread Title'
        })
        self.assertTrue(form.is_valid())


# Test the form which creates a new post.
class PostFormTest(TestCase):
    def test_post_form(self):
        form = PostForm({
            'content': 'The content of the post.'
        })
        self.assertTrue(form.is_valid())
