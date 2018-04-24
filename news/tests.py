# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.test import TestCase
from .views import news_index, news_item, news_team, blog_home, blog_index, blog_post, new_blog_post, new_comment, \
    delete_comment, edit_comment
from django.core.urlresolvers import resolve
from .forms import CommentForm, BlogPostForm


# Tests the main news index.
class NewsIndexTest(TestCase):
    def test_news_index_resolves(self):
        news_home = resolve('/news/')
        self.assertEqual(news_home.func, news_index)

    def test_news_index_code(self):
        news_home = self.client.get('/news/')
        self.assertEqual(news_home.status_code, 200)

    def test_news_index_content(self):
        news_home = self.client.get('/news/')
        self.assertTemplateUsed(news_home, 'news.html')


# Tests an individual news story.
class NewsItemTest(TestCase):

    fixtures = ['news', 'users', 'teams']

    def test_news_item_resolves(self):
        article = resolve('/news/1/')
        self.assertEqual(article.func, news_item)

    def test_news_item_code(self):
        article = self.client.get('/news/1/')
        self.assertEqual(article.status_code, 200)

    def test_news_item_content(self):
        article = self.client.get('/news/1/')
        self.assertTemplateUsed(article, 'news_item.html')


# Tests an team news page.
class NewsTeamTest(TestCase):
    def test_news_team_resolves(self):
        team_news = resolve('/news/manchester/')
        self.assertEqual(team_news.func, news_team)


# Test the fan blogs home page.
class BlogHomeTest(TestCase):

    fixtures = ['auth']

    def test_blog_home_resolves(self):
        blogs_home = resolve('/blogs/')
        self.assertEqual(blogs_home.func, blog_home)

    def test_news_index_code(self):
        blogs_home = self.client.get('/blogs/')
        self.assertEqual(blogs_home.status_code, 200)

    def test_news_index_content(self):
        blogs_home = self.client.get('/blogs/')
        self.assertTemplateUsed(blogs_home, 'blogs.html')


# Test an individual user's blog.
class BlogIndexTest(TestCase):
    def test_blog_index_resolves(self):
        user_blog = resolve('/blogs/user/admin/')
        self.assertEqual(user_blog.func, blog_index)


# Test an individual blog post.
class BlogPostTest(TestCase):
    def test_blog_post_resolves(self):
        individual_blog = resolve('/blogs/post/1/')
        self.assertEqual(individual_blog.func, blog_post)


# Test the new blog post view.
class NewBlogTest(TestCase):
    def test_new_blog_post_resolves(self):
        new_blog = resolve('/blogs/post/new/')
        self.assertEqual(new_blog.func, new_blog_post)


# Test the view that adds a new comment.
class NewCommentTest(TestCase):
    def test_new_comment_resolves(self):
        add_comment = resolve('/comment/new/1/')
        self.assertEqual(add_comment.func, new_comment)


# Test the view that edits a comment.
class EditCommentTest(TestCase):
    def test_edit_comment_resolves(self):
        change_comment = resolve('/comment/edit/1/1/')
        self.assertEqual(change_comment.func, edit_comment)


# Test the view that deletes a comment.
class DeleteCommentTest(TestCase):
    def test_delete_comment_resolves(self):
        remove_comment = resolve('/comment/delete/1/1/')
        self.assertEqual(remove_comment.func, delete_comment)


# Test the new comment form.
class CommentFormTest(TestCase):

    def test_comment_form(self):
        form = CommentForm({
            'comment': 'The content of the comment.'
        })
        self.assertTrue(form.is_valid())


# Test the blog post form.
class BlogPostFormTest(TestCase):
    def test_blog_post_form(self):
        form = BlogPostForm({
            'title': 'Post Title',
            'content': 'The content of the post.'
        })
        self.assertTrue(form.is_valid())
