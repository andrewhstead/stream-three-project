# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from news.models import Item
from .forms import MessageForm
from django.template.context_processors import csrf
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.shortcuts import redirect


# Create your views here.
def home_page(request):

    user = request.user
    news_headlines = Item.objects.exclude(category_id=6).order_by('-created_date')[:7]

    if user.is_authenticated:
        favourite_team = user.favourite_team
        if favourite_team:
            extra_news = Item.objects.filter(teams=favourite_team.id).order_by('-created_date')[:5]

            return render(request, "home.html", {"news_headlines": news_headlines, "favourite_team": favourite_team,
                                                 "extra_news": extra_news})
        else:
            extra_news = Item.objects.exclude(category_id=6).order_by('-created_date')[7:12]

            return render(request, "home.html", {"news_headlines": news_headlines, "extra_news": extra_news})

    else:
        extra_news = Item.objects.exclude(category_id=6).order_by('-created_date')[7:12]

        return render(request, "home.html", {"news_headlines": news_headlines, "extra_news": extra_news})


def contact(request):

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your message has been sent!")

        return redirect(reverse('home'))

    else:
        form = MessageForm()

    args = {
        'form': form,
        'button_text': 'Send Message'
    }
    args.update(csrf(request))

    return render(request, 'contact.html', args)
