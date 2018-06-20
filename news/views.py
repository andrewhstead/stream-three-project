# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404, redirect
from .models import Item, Comment, list_bloggers
from .forms import BlogPostForm, CommentForm
from teams.models import Team
from users.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.template.context_processors import csrf
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.models import Group


# Create your views here.
# Display a full list of all news items, with the exception of blog posts.
def news_index(request):
    # Remove blog posts from the news view, as they will be displayed separately.
    all_items = Item.objects.exclude(category_id=6).order_by('-created_date')

    # Use pagination to display 20 headlines at a time.
    page_items = Paginator(all_items, 20)

    page = request.GET.get('page')

    if page:
        current_page = int(page)
    else:
        current_page = 1

    page_count = page_items.num_pages

    try:
        items = page_items.page(page)
    except EmptyPage:
        items = page_items.page(page_count)
    except PageNotAnInteger:
        items = page_items.page(1)

    # The page is neither an archive page nor a team page.
    archive = False
    team = False

    return render(request, "news.html", {"items": items, "current_page": current_page,
                                         "page_count": page_count, 'archive': archive,
                                         'team': team})


# Display an individual news story, incrementing its post count each time it is loaded.
def news_item(request, news_id):
    item = get_object_or_404(Item, pk=news_id)
    item.views += 1
    item.save()

    # The page is neither an archive page nor a team page.
    archive = False
    team = False

    return render(request, "news_item.html", {"item": item, 'archive': archive, 'team': team})


# Display a team news page, with just stories in which the chosen team is tagged.
def news_team(request, team_name):
    team = get_object_or_404(Team, geographic_name=team_name.capitalize())
    all_items = Item.objects.filter(teams=team.id).order_by('-created_date')

    # Use pagination to display 20 headlines at a time.
    page_items = Paginator(all_items, 20)

    page = request.GET.get('page')

    if page:
        current_page = int(page)
    else:
        current_page = 1

    page_count = page_items.num_pages

    try:
        items = page_items.page(page)
    except EmptyPage:
        items = page_items.page(page_count)
    except PageNotAnInteger:
        items = page_items.page(1)

    # The page is not archive page.
    archive = False

    return render(request, "news_team.html", {'team': team, 'items': items, 'archive': archive,
                                              'current_page': current_page})


# Display the home page of the fan blogs section.
def blog_home(request):
    # Use the category_id for blog posts to select the news items in that catgory.
    blog_posts = Item.objects.filter(category_id=6).order_by('-created_date')

    # Obtain the list of bloggers.
    bloggers = list_bloggers()

    # Pagination to show five posts at a time.
    posts_for = Paginator(blog_posts, 5)

    page = request.GET.get('page')
    try:
        posts = posts_for.page(page)
    except EmptyPage:
        posts = posts_for.page(posts_for.num_pages)
    except PageNotAnInteger:
        posts = posts_for.page(1)

    if page:
        current_page = int(page)
    else:
        current_page = 1

    return render(request, "blogs.html", {'posts': posts, 'bloggers': bloggers, 'current_page': current_page})


# The home page for an individual blog.
def blog_index(request, author_name):
    # Get the user and filter out only those posts they have made.
    author = User.objects.get(username__iexact=author_name)
    all_posts = Item.objects.filter(author=author).order_by('-created_date')

    bloggers = list_bloggers()

    # Show 10 posts at a time using pagination.
    posts_for = Paginator(all_posts, 10)

    page = request.GET.get('page')
    try:
        posts = posts_for.page(page)
    except EmptyPage:
        posts = posts_for.page(1)
    except PageNotAnInteger:
        posts = posts_for.page(posts_for.num_pages)

    return render(request, "blog_index.html", {'all_posts': all_posts, 'posts': posts,
                                               'author': author, 'bloggers': bloggers})


# Show an individual blog post, incrementing its view count by one for each view.
def blog_post(request, post_id):
    item = Item.objects.get(pk=post_id)
    posts = Item.objects.filter(author=item.author).order_by('-created_date')
    item.views += 1
    item.save()

    bloggers = list_bloggers()

    return render(request, "blog_post.html", {'item': item, 'posts': posts, 'bloggers': bloggers})


# The form that allows an authorised blogger to create a new post.
@login_required(login_url='/login/')
def new_blog_post(request):
    user = request.user

    if request.method == 'POST':
        form = BlogPostForm(request.POST)
        if form.is_valid():
            # Do not save the post until it has been allocated to the user and given the right category for a blog post.
            new_post = form.save(False)
            new_post.author = user
            new_post.category_id = 6
            new_post.save()
            messages.success(request, "Your blog post has been added!")

            return redirect(reverse('blog_post', args={new_post.pk}))

    else:
        form = BlogPostForm()

    bloggers = list_bloggers()

    args = {
        'form': form,
        'form_action': reverse('new_blog_post'),
        'button_text': 'Submit Post',
        'bloggers': bloggers
    }
    args.update(csrf(request))
    return render(request, 'blog_post_form.html', args)


# Edit an existing blog post.
@login_required(login_url='/login/')
def edit_blog(request, post_id):
    post = get_object_or_404(Item, pk=post_id)

    if request.method == 'POST':
        form = BlogPostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save()
            messages.success(request, "Your blog post has been edited.")

            return redirect(reverse('blog_post', args={post.pk}))

    else:
        form = BlogPostForm(instance=post)

    bloggers = list_bloggers()

    args = {
        'form': form,
        'post': post,
        'form_action': reverse('edit_blog', kwargs={'post_id': post.id}),
        'button_text': 'Submit Post',
        'bloggers': bloggers
    }
    args.update(csrf(request))
    return render(request, 'blog_post_form.html', args)


# Delete an unwanted blog post.
@login_required(login_url='/login/')
def delete_blog(request, post_id):
    post = get_object_or_404(Item, pk=post_id)

    post.delete()

    messages.success(request, "Your post has been deleted.")

    return redirect(reverse('blog_home'))


# Add a new comment to a news story or a blog post.
@login_required(login_url='/login/')
def new_comment(request, item_id):
    item = get_object_or_404(Item, pk=item_id)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            # Don't save until the comment has been allocated to the right user and the right news story.
            comment = form.save(False)
            comment.user = request.user
            comment.item = item
            comment.save()
            messages.success(request, "Your comment has been added!")

            if item.category.name == 'Blog Posts':
                return redirect(reverse('blog_post', args={item.pk}))
            else:
                return redirect(reverse('news', args={item.pk}))

    else:
        form = CommentForm()

    bloggers = list_bloggers()

    args = {
        'form': form,
        'form_action': reverse('new_comment', args={item.id}),
        'button_text': 'Post Comment',
        'bloggers': bloggers
    }
    args.update(csrf(request))
    return render(request, 'comment_form.html', args)


# Edit an existing comment.
@login_required(login_url='/login/')
def edit_comment(request, item_id, comment_id):
    item = get_object_or_404(Item, pk=item_id)
    comment = get_object_or_404(Comment, pk=comment_id)

    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            messages.success(request, "Your comment has been successfully edited.")

            if item.category.name == 'Blog Posts':
                return redirect(reverse('blog_post', args={item.pk}))
            else:
                return redirect(reverse('news', args={item.pk}))

    else:
        form = CommentForm(instance=comment)

    bloggers = list_bloggers()

    args = {
        'form': form,
        'form_action': reverse('edit_comment', kwargs={'item_id': item.id, 'comment_id': comment.id}),
        'button_text': 'Edit Comment',
        'bloggers': bloggers,
        'comment': comment
    }
    args.update(csrf(request))
    return render(request, 'comment_form.html', args)


# Delete a comment.
@login_required(login_url='/login/')
def delete_comment(request, item_id, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    item = get_object_or_404(Item, pk=item_id)

    comment.delete()
    messages.success(request, "Your comment was deleted.")

    return redirect(reverse('news', args={item.pk}))

