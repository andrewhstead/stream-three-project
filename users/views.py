# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, get_object_or_404
from django.template.context_processors import csrf
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from .forms import LoginForm, RegistrationForm
from comments.models import Comment
from users.models import User


# Create your views here.
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            user = auth.authenticate(username=request.POST.get('username'),
                                     password=request.POST.get('password1'))

            if user:
                messages.success(request, 'Registration successful!')
                auth.login(request, user)
                return redirect(reverse('user_profile'))
            else:
                messages.error(request, 'Sorry, we were unable to register your account. Please try again.')

    else:
        form = RegistrationForm()

    args = {'form': form}
    args.update(csrf(request))
    return render(request, 'register.html', args)


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = auth.authenticate(username=request.POST.get('username'),
                                     password=request.POST.get('password'))

            if user is not None:
                auth.login(request, user)
                return redirect(reverse('user_profile'))
            else:
                form.add_error(None, "Your username or password was not recognised. Please try again.")

    else:
        form = LoginForm()

    args = {'form': form}
    args.update(csrf(request))
    return render(request, 'login.html', args)


def logout(request):
    auth.logout(request)
    return redirect(reverse('login'))


@login_required(login_url='/login/')
def user_profile(request):
    user = request.user
    comments = Comment.objects.filter(user_id=user.id)
    return render(request, 'profile.html', {'comments': comments, 'profile_user': user})


@login_required(login_url='/login/')
def other_profile(request, user_id):
    user = request.user
    profile_user = get_object_or_404(User, pk=user_id)
    comments = Comment.objects.filter(user_id=profile_user.id)

    if user == profile_user:
        return redirect(reverse('user_profile'))

    else:
        return render(request, 'profile.html', {'comments': comments, 'profile_user': profile_user})
