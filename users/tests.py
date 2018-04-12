# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.test import TestCase
from .views import register, login, logout, user_profile, other_profile,\
    edit_profile, delete_profile, change_password
from django.core.urlresolvers import resolve


class RegisterTest(TestCase):
    def test_register_resolves(self):
        registration = resolve('/register/')
        self.assertEqual(registration.func, register)


class LoginTest(TestCase):
    def test_login_resolves(self):
        user_login = resolve('/login/')
        self.assertEqual(user_login.func, login)


class LogoutTest(TestCase):
    def test_logout_resolves(self):
        user_logout = resolve('/logout/')
        self.assertEqual(user_logout.func, logout)


class UserProfileTest(TestCase):
    def test_user_profile_resolves(self):
        profile = resolve('/profile/')
        self.assertEqual(profile.func, user_profile)


class OtherProfileTest(TestCase):
    def test_other_profile_resolves(self):
        other_user = resolve('/profile/2/')
        self.assertEqual(other_user.func, other_profile)


class EditProfileTest(TestCase):
    def test_edit_profile_resolves(self):
        profile_change = resolve('/profile/edit/')
        self.assertEqual(profile_change.func, edit_profile)


class DeleteProfileTest(TestCase):
    def test_delete_profile_resolves(self):
        account_delete = resolve('/profile/delete/')
        self.assertEqual(account_delete.func, delete_profile)


class ChangePassword(TestCase):
    def test_change_password_resolves(self):
        new_password = resolve('/profile/password/')
        self.assertEqual(new_password.func, change_password)
