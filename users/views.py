# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.template.context_processors import csrf
from django.contrib import auth
from django.core.urlresolvers import reverse
from .forms import LoginForm


# Create your views here.
def register(request):
    return render(request, 'register.html')


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = auth.authenticate(username=request.POST.get('username'),
                                     password=request.POST.get('password'))

            if user is not None:
                auth.login(request, user)
                return redirect(reverse('standings'))
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


def profile(request):
    return render(request, 'user_profile.html')
