# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.test import TestCase
from .views import register, login, logout, user_profile, other_profile,\
    edit_profile, delete_profile, change_password
from django.core.urlresolvers import resolve
from django.contrib.auth.models import Group
from django import forms
from .models import User
from .forms import EditProfileForm, DeletionForm, ChangePasswordForm, LoginForm, RegistrationForm


class RegisterTest(TestCase):
    def test_register_resolves(self):
        registration = resolve('/register/')
        self.assertEqual(registration.func, register)

    def test_register_status_code(self):
        registration = self.client.get('/register/')
        self.assertEqual(registration.status_code, 200)

    def test_register_content(self):
        registration = self.client.get('/register/')
        self.assertTemplateUsed(registration, 'user_details.html')


class LoginTest(TestCase):
    def test_login_resolves(self):
        user_login = resolve('/login/')
        self.assertEqual(user_login.func, login)

    def test_login_status_code(self):
        user_login = self.client.get('/login/')
        self.assertEqual(user_login.status_code, 200)

    def test_login_content(self):
        user_login = self.client.get('/login/')
        self.assertTemplateUsed(user_login, 'login.html')


class LogoutTest(TestCase):
    def test_logout_resolves(self):
        user_logout = resolve('/logout/')
        self.assertEqual(user_logout.func, logout)

    def test_logout_status_code(self):
        user_logout = self.client.get('/logout/')
        self.assertEqual(user_logout.status_code, 302)


class UserProfileTest(TestCase):
    fixtures = ['users', 'teams', 'auth', 'store']

    def setUp(self):
        super(UserProfileTest, self).setUp()
        self.user = User.objects.create(username='username')
        self.user.set_password('password')
        self.user.save()

    def test_user_profile_resolves(self):
        profile = resolve('/profile/')
        self.assertEqual(profile.func, user_profile)

    def test_user_profile_status_code(self):
        self.client.login(username='username', password='password')
        profile = self.client.get('/profile/')
        self.assertEqual(profile.status_code, 200)

    def test_user_profile_content(self):
        self.client.login(username='username', password='password')
        profile = self.client.get('/profile/')
        self.assertTemplateUsed(profile, 'profile.html')


class OtherProfileTest(TestCase):
    fixtures = ['users', 'teams', 'auth', 'store']

    def setUp(self):
        super(OtherProfileTest, self).setUp()
        self.user = User.objects.create(username='username')
        self.user.set_password('password')
        self.user.save()

    def test_other_profile_resolves(self):
        other_user = resolve('/profile/2/')
        self.assertEqual(other_user.func, other_profile)

    # def test_other_profile_status_code(self):
    #     self.client.login(username='username', password='password')
    #     other_user = self.client.get('/profile/2/')
    #     self.assertEqual(other_user.status_code, 200)
    #
    # def test_other_profile_content(self):
    #     self.client.login(username='username', password='password')
    #     other_user = self.client.get('/profile/2/')
    #     self.assertTemplateUsed(other_user, 'profile.html')


class EditProfileTest(TestCase):

    def setUp(self):
        super(EditProfileTest, self).setUp()
        self.user = User.objects.create(username='username')
        self.user.set_password('password')
        self.user.save()

    def test_edit_profile_resolves(self):
        profile_change = resolve('/profile/edit/')
        self.assertEqual(profile_change.func, edit_profile)

    def test_edit_profile_status_code(self):
        self.client.login(username='username', password='password')
        profile_change = self.client.get('/profile/edit/')
        self.assertEqual(profile_change.status_code, 200)

    def test_edit_profile_content(self):
        self.client.login(username='username', password='password')
        profile_change = self.client.get('/profile/edit/')
        self.assertTemplateUsed(profile_change, 'user_details.html')


class DeleteProfileTest(TestCase):

    def setUp(self):
        super(DeleteProfileTest, self).setUp()
        self.user = User.objects.create(username='username')
        self.user.set_password('password')
        self.user.save()

    def test_delete_profile_resolves(self):
        account_delete = resolve('/profile/delete/')
        self.assertEqual(account_delete.func, delete_profile)

    def test_delete_profile_status_code(self):
        self.client.login(username='username', password='password')
        account_delete = self.client.get('/profile/delete/')
        self.assertEqual(account_delete.status_code, 200)

    def test_delete_profile_content(self):
        self.client.login(username='username', password='password')
        account_delete = self.client.get('/profile/delete/')
        self.assertTemplateUsed(account_delete, 'delete_profile.html')


class ChangePasswordTest(TestCase):

    def setUp(self):
        super(ChangePasswordTest, self).setUp()
        self.user = User.objects.create(username='username')
        self.user.set_password('password')
        self.user.save()

    def test_change_password_resolves(self):
        new_password = resolve('/profile/password/')
        self.assertEqual(new_password.func, change_password)

    def test_change_password_status_code(self):
        self.client.login(username='username', password='password')
        new_password = self.client.get('/profile/password/')
        self.assertEqual(new_password.status_code, 200)

    def test_change_password_content(self):
        self.client.login(username='username', password='password')
        new_password = self.client.get('/profile/password/')
        self.assertTemplateUsed(new_password, 'change_password.html')


class LoginFormTest(TestCase):
    def test_login_form(self):
        form = LoginForm({
            'username': 'username',
            'password': 'password'
        })
        self.assertTrue(form.is_valid())

    def test_login_form_fails(self):
        form = LoginForm({})
        self.assertFalse(form.is_valid())


class RegistrationFormTest(TestCase):
    def test_registration_form(self):
        form = RegistrationForm({
            'username': 'username',
            'email': 'user@user.com',
            'password1': 'password',
            'password2': 'password'
        })
        self.assertTrue(form.is_valid())

    def test_registration_form_fails_different_passwords(self):
        form = RegistrationForm({
            'username': 'username',
            'email': 'user@user.com',
            'password1': 'password1',
            'password2': 'password2'
        })
        self.assertFalse(form.is_valid())
        self.assertRaisesMessage(forms.ValidationError,
                                 "Your passwords do not match. Please try again.",
                                 form.full_clean())


class ChangePasswordFormTest(TestCase):
    def test_change_password_form(self):
        form = ChangePasswordForm({
            'password': 'password',
            'password1': 'password1',
            'password2': 'password1'
        })
        self.assertTrue(form.is_valid())

    def test_change_password_form_fails_different_passwords(self):
        form = ChangePasswordForm({
            'password': 'password',
            'password1': 'password1',
            'password2': 'password2'
        })
        self.assertFalse(form.is_valid())
        self.assertRaisesMessage(forms.ValidationError,
                                 "Your passwords do not match. Please try again.",
                                 form.full_clean())


class EditProfileFormTest(TestCase):
    def test_edit_profile_form(self):
        form = EditProfileForm({
            'username': 'username',
            'first_name': 'User',
            'last_name': 'Name',
            'email': 'user@user.com',
        })
        self.assertTrue(form.is_valid())


class DeleteProfileFormTest(TestCase):
    def test_delete_profile_form(self):
        form = DeletionForm({
            'password': 'password'
        })
        self.assertTrue(form.is_valid())
