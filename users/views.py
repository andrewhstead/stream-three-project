# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, get_object_or_404
from django.template.context_processors import csrf
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from .forms import LoginForm, RegistrationForm, EditProfileForm, DeletionForm, ChangePasswordForm
from comments.models import Comment
from forum.models import Thread, Post
from store.models import Cart
from .models import User


# Create your views here.
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            user = auth.authenticate(username=request.POST.get('username'),
                                     password=request.POST.get('password1'))

            if user:
                messages.success(request, 'Your registration was successful!')
                auth.login(request, user)
                return redirect(reverse('user_profile'))
            else:
                messages.error(request, 'Sorry, we were unable to register your account. Please try again.')

    else:
        form = RegistrationForm()

    args = {
        'form': form,
        'button_text': 'Register',
    }
    args.update(csrf(request))
    return render(request, 'user_details.html', args)


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = auth.authenticate(username=request.POST.get('username'),
                                     password=request.POST.get('password'))

            if user is not None:
                auth.login(request, user)
                messages.success(request, "You have successfully logged in!")
                return redirect(reverse('user_profile'))
            else:
                messages.error(request, "Your username or password was not recognised. Please try again.")

    else:
        form = LoginForm()

    args = {'form': form}
    args.update(csrf(request))
    return render(request, 'login.html', args)


def logout(request):
    auth.logout(request)
    messages.success(request, 'You have successfully logged out.')

    return redirect(reverse('login'))


@login_required(login_url='/login/')
def user_profile(request):
    user = request.user
    comments = Comment.objects.filter(user_id=user.id)
    posts = Post.objects.filter(user_id=user.id)
    threads = Thread.objects.filter(user_id=user.id)
    orders = Cart.objects.filter(user_id=user.id, status='Received')

    contributions = []

    for comment in comments:
        contributions.append(comment)

    for post in posts:
        contributions.append(post)

    return render(request, 'profile.html', {'comments': comments, 'threads': threads,
                                            'posts': posts, 'contributions': contributions,
                                            'profile_user': user, 'orders': orders})


@login_required(login_url='/login/')
def other_profile(request, user_id):
    user = request.user
    profile_user = get_object_or_404(User, pk=user_id)
    comments = Comment.objects.filter(user_id=profile_user.id)
    posts = Post.objects.filter(user_id=profile_user.id)
    threads = Thread.objects.filter(user_id=profile_user.id)
    contributions = []

    for comment in comments:
        contributions.append(comment)

    for post in posts:
        contributions.append(post)

    if user == profile_user:
        return redirect(reverse('user_profile'))

    else:
        return render(request, 'profile.html', {'comments': comments, 'threads': threads,
                                                'posts': posts, 'contributions': contributions,
                                                'profile_user': profile_user})


@login_required(login_url='/login/')
def edit_profile(request):
    user = request.user

    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated.')
            return redirect(reverse('user_profile'))
        else:
            messages.error(request, 'Sorry, we were unable to update your details. Please try again.')

    else:
        form = EditProfileForm(instance=user)

    args = {
        'form': form,
        'button_text': 'Update Profile',
    }
    args.update(csrf(request))
    return render(request, 'user_details.html', args)


@login_required(login_url='/login/')
def delete_profile(request):
    user = request.user

    if request.method == 'POST':
        form = DeletionForm(request.POST)
        if form.is_valid():
            user_to_delete = auth.authenticate(username=user.username,
                                               password=request.POST.get('password'))
            if user_to_delete is not None:
                user_to_delete.delete()
                messages.success(request, 'Your profile has been deleted.')
                return redirect(reverse('login'))
            else:
                messages.error(request, 'Your password was not recognised. Please try again.')

    else:
        form = DeletionForm()

    args = {
        'form': form,
        'button_text': 'Delete Account',
    }
    args.update(csrf(request))
    return render(request, 'delete_profile.html', args)


@login_required(login_url='/login/')
def change_password(request):
    user = request.user

    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)

        if form.is_valid():
            user_to_change = auth.authenticate(username=user.username,
                                               password=request.POST.get('password'))

            if user_to_change is not None:
                user.set_password(request.POST.get('newpassword1'))
                user.save()
                auth.login(request, user)
                messages.success(request, 'Your password has been changed.')
                return redirect(reverse('user_profile'))

            else:
                messages.error(request, 'Sorry, we were unable to change your password. Please try again.')

    else:
        form = ChangePasswordForm()

    args = {
        'form': form,
        'button_text': 'Change Password',
    }
    args.update(csrf(request))
    return render(request, 'change_password.html', args)
