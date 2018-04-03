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
            messages.success(request, "Your comment has been added!")

        return redirect(reverse('news', args={item.pk}))

    else:
        form = CommentForm()

    args = {
        'form': form,
        'form_action': reverse('new_comment', args={item.id}),
        'button_text': 'Post Comment'
    }
    args.update(csrf(request))
    return render(request, 'comment_form.html', args)


@login_required
def edit_comment(request, item_id, comment_id):
    item = get_object_or_404(Item, pk=item_id)
    comment = get_object_or_404(Comment, pk=comment_id)

    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            messages.success(request, "Your comment has been successfully edited.")

        return redirect(reverse('news', args={item.pk}))

    else:
        form = CommentForm(instance=comment)

    args = {
        'form': form,
        'form_action': reverse('edit_comment', kwargs={'item_id': item.id, 'comment_id': comment.id}),
        'button_text': 'Edit Comment',
        'comment': comment
    }
    args.update(csrf(request))
    return render(request, 'comment_form.html', args)


@login_required
def delete_comment(request, item_id, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    item = get_object_or_404(Item, pk=item_id)

    comment.delete()
    messages.success(request, "Your comment was deleted.")

    return redirect(reverse('news', args={item.pk}))
