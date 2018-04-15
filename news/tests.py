# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.test import TestCase
from .views import news_index, news_item, news_team, blog_home, blog_index, blog_post, new_blog_post
from django.core.urlresolvers import resolve
from django.shortcuts import render_to_response


class LastNextTest(TestCase):
    def test_news_index_resolves(self):
        news_home = resolve('/news/')
        self.assertEqual(news_home.func, news_index)

    def test_news_index_code(self):
        news_home = self.client.get('/news/')
        self.assertEqual(news_home.status_code, 200)

    def test_news_index_content(self):
        news_home = self.client.get('/news/')
        self.assertTemplateUsed(news_home, 'news.html')


class NewsItemTest(TestCase):
    def test_news_item_resolves(self):
        article = resolve('/news/1/')
        self.assertEqual(article.func, news_item)

    # def test_news_item_code(self):
    #     article = self.client.get('/news/1/')
    #     self.assertEqual(article.status_code, 200)
    #
    # def test_news_item_content(self):
    #     article = self.client.get('/news/1/')
    #     self.assertTemplateUsed(article, 'news_item.html')


class NewsTeamTest(TestCase):
    def test_news_team_resolves(self):
        team_news = resolve('/news/manchester/')
        self.assertEqual(team_news.func, news_team)


class BlogHomeTest(TestCase):
    def test_blog_home_resolves(self):
        blogs_home = resolve('/blogs/')
        self.assertEqual(blogs_home.func, blog_home)

    def test_news_index_code(self):
        blogs_home = self.client.get('/blogs/')
        self.assertEqual(blogs_home.status_code, 200)

    def test_news_index_content(self):
        blogs_home = self.client.get('/blogs/')
        self.assertTemplateUsed(blogs_home, 'blogs.html')


class BlogIndexTest(TestCase):
    def test_blog_index_resolves(self):
        user_blog = resolve('/blogs/user/admin/')
        self.assertEqual(user_blog.func, blog_index)


class BlogPostTest(TestCase):
    def test_blog_post_resolves(self):
        individual_blog = resolve('/blogs/post/1/')
        self.assertEqual(individual_blog.func, blog_post)


class NewBlogTest(TestCase):
    def test_new_blog_post_resolves(self):
        new_blog = resolve('/blogs/post/new/')
        self.assertEqual(new_blog.func, new_blog_post)


# class EditBlogTest(TestCase):
#     def test_edit_blog_resolves(self):
#         edit_blog = resolve('/blogs/post/edit/152/')
#         self.assertEqual(edit_blog.func, edit_blog)
#
#
# class DeleteBlogTest(TestCase):
#     def test_delete_blog_resolves(self):
#         delete_blog = resolve('/blogs/post/delete/152/')
#         self.assertEqual(delete_blog.func, delete_blog)
