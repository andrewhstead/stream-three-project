# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from .views import forum_home, forum_league, forum_team, new_thread, view_thread, new_post, edit_post, delete_post
from django.core.urlresolvers import resolve
from .forms import ThreadForm, PostForm
from users.models import User


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

    fixtures = ['forum', 'teams', 'users']

    def test_league_forum_resolves(self):
        message_board = resolve('/forum/league/1/')
        self.assertEqual(message_board.func, forum_league)

    def test_league_forum_code(self):
        message_board = self.client.get('/forum/league/1/')
        self.assertEqual(message_board.status_code, 200)

    def test_league_forum_content(self):
        message_board = self.client.get('/forum/league/1/')
        self.assertTemplateUsed(message_board, 'board.html')


# Test a team-specific message board.
class TeamForumTest(TestCase):

    fixtures = ['forum', 'teams', 'users']

    def test_team_forum_resolves(self):
        message_board = resolve('/forum/birmingham/')
        self.assertEqual(message_board.func, forum_team)

    def test_team_forum_code(self):
        message_board = self.client.get('/forum/birmingham/')
        self.assertEqual(message_board.status_code, 200)

    def test_team_forum_content(self):
        message_board = self.client.get('/forum/birmingham/')
        self.assertTemplateUsed(message_board, 'board.html')


# Test the view which shows the user a single thread.
class ViewThreadTest(TestCase):

    fixtures = ['forum', 'teams', 'users']

    def test_view_thread_resolves(self):
        thread_view = resolve('/thread/1/')
        self.assertEqual(thread_view.func, view_thread)

    def test_view_thread_code(self):
        thread_view = self.client.get('/thread/1/')
        self.assertEqual(thread_view.status_code, 200)

    def test_view_thread_content(self):
        thread_view = self.client.get('/thread/1/')
        self.assertTemplateUsed(thread_view, 'thread.html')


# Test the view which allows a new thread to be created.
class NewThreadTest(TestCase):

    fixtures = ['forum', 'teams', 'users']

    def setUp(self):
        super(NewThreadTest, self).setUp()
        self.user = User.objects.create(username='username')
        self.user.set_password('password')
        self.user.save()

    def test_new_thread_resolves(self):
        thread_start = resolve('/thread/new/1/')
        self.assertEqual(thread_start.func, new_thread)

    def test_new_thread_code(self):
        self.client.login(username='username', password='password')
        thread_start = self.client.get('/thread/new/1/')
        self.assertEqual(thread_start.status_code, 200)

    def test_new_thread_content(self):
        self.client.login(username='username', password='password')
        thread_start = self.client.get('/thread/new/1/')
        self.assertTemplateUsed(thread_start, 'thread_form.html')


# Test the view for creating a new post in a thread.
class NewPostTest(TestCase):

    fixtures = ['forum', 'teams', 'users']

    def setUp(self):
        super(NewPostTest, self).setUp()
        self.user = User.objects.create(username='username')
        self.user.set_password('password')
        self.user.save()

    def test_new_post_resolves(self):
        add_post = resolve('/post/new/1/')
        self.assertEqual(add_post.func, new_post)

    def test_new_post_code(self):
        self.client.login(username='username', password='password')
        add_post = self.client.get('/post/new/1/')
        self.assertEqual(add_post.status_code, 200)

    def test_new_post_content(self):
        self.client.login(username='username', password='password')
        add_post = self.client.get('/post/new/1/')
        self.assertTemplateUsed(add_post, 'post_form.html')


# Test the view for editing a forum post.
class EditPostTest(TestCase):

    fixtures = ['forum', 'teams', 'users']

    def setUp(self):
        super(EditPostTest, self).setUp()
        self.user = User.objects.create(username='username')
        self.user.set_password('password')
        self.user.save()

    def test_edit_post_resolves(self):
        change_post = resolve('/post/edit/1/1/')
        self.assertEqual(change_post.func, edit_post)

    def test_edit_post_code(self):
        self.client.login(username='username', password='password')
        change_post = self.client.get('/post/edit/1/1/')
        self.assertEqual(change_post.status_code, 200)

    def test_edit_post_content(self):
        self.client.login(username='username', password='password')
        change_post = self.client.get('/post/edit/1/1/')
        self.assertTemplateUsed(change_post, 'post_form.html')


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
