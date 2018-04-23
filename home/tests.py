# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from home.views import home_page
from django.core.urlresolvers import resolve
from django.shortcuts import render_to_response
from .forms import MessageForm


class HomePageTest(TestCase):

    def test_home_page_resolves(self):
        site_home = resolve('/')
        self.assertEqual(site_home.func, home_page)

    def test_home_page_status_code_is_ok(self):
        site_home = self.client.get('/')
        self.assertEqual(site_home.status_code, 200)

    def test_check_content_is_correct(self):
        site_home = self.client.get('/')
        self.assertTemplateUsed(site_home, "home.html")
        site_home_template_output = render_to_response("home.html").content
        self.assertEqual(site_home.content, site_home_template_output)


class ContactFormTest(TestCase):
    def test_message_form(self):
        form = MessageForm({
            'sender': 'Sender Name',
            'email': 'email@address.me ',
            'subject': 'Message Subject',
            'message': 'The content of the message.'
        })
        self.assertTrue(form.is_valid())
