# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from .views import new_comment, edit_comment, delete_comment
from django.core.urlresolvers import resolve
from .forms import CommentForm


class NewCommentTest(TestCase):
    def test_new_comment_resolves(self):
        add_comment = resolve('/comment/new/1/')
        self.assertEqual(add_comment.func, new_comment)


class EditCommentTest(TestCase):
    def test_edit_comment_resolves(self):
        change_comment = resolve('/comment/edit/1/1/')
        self.assertEqual(change_comment.func, edit_comment)


class DeleteCommentTest(TestCase):
    def test_delete_comment_resolves(self):
        remove_comment = resolve('/comment/delete/1/1/')
        self.assertEqual(remove_comment.func, delete_comment)


class CommentFormTest(TestCase):
    def test_comment_form(self):
        form = CommentForm({
            'comment': 'The content of the comment.'
        })
        self.assertTrue(form.is_valid())

