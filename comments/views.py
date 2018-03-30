# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404
from news.models import Item
from django.contrib.auth.decorators import login_required
from django.template.context_processors import csrf
from .forms import CommentForm
from .models import Comment
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.http import HttpResponse


# Create your views here.
@login_required
def new_comment(request, item_id):
    item = get_object_or_404(Item, pk=item_id)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(False)
            comment.user = request.user
            comment.item = item
            comment.save()

        return redirect(reverse('news', args={item.pk}))

    else:
        form = CommentForm()

    args = {
        'form': form,
        'form_action': reverse('new_comment', args={item.id}),
    }
    args.update(csrf(request))
    return render(request, 'new_comment.html', args)


def vote_up(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    comment.rating += 1
    comment.save()

    return HttpResponse('')
