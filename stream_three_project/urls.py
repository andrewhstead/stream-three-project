"""stream_three_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from home import views as home_views
from news import views as news_views
from games import views as games_views
from teams import views as team_views
from forum import views as forum_views
from users import views as users_views
from comments import views as comments_views
from django.views.static import serve
from .settings import MEDIA_ROOT

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', home_views.home_page),
    url(r'^archive/$', games_views.season_archive, name='archive'),
    url(r'^comment/new/(?P<item_id>\d+)/$', comments_views.new_comment, name='new_comment'),
    url(r'^comment/edit/(?P<item_id>\d+)/(?P<comment_id>\d+)/$',
        comments_views.edit_comment, name='edit_comment'),
    url(r'^comment/delete/(?P<item_id>\d+)/(?P<comment_id>\d+)/$',
        comments_views.delete_comment, name='delete_comment'),
    url(r'^forum/$', forum_views.forum_home, name='forum'),
    url(r'^forum/league/(?P<board_id>\d+)/$', forum_views.forum_league, name='forum_league'),
    url(r'^forum/(?P<team_name>.*)/$', forum_views.forum_team, name='forum_team'),
    url(r'^login/$', users_views.login, name="login"),
    url(r'^logout/$', users_views.logout, name="logout"),
    url(r'^media/(?P<path>.*)$', serve, {'document_root': MEDIA_ROOT}),
    url(r'^news/$', news_views.news_index),
    url(r'^news/(?P<news_id>\d+)/$', news_views.news_item, name='news'),
    url(r'^news/(?P<team_name>.*)/$', news_views.news_team, name='team_news'),
    url(r'^profile/$', users_views.user_profile, name='user_profile'),
    url(r'^profile/delete/$', users_views.delete_profile, name='delete_profile'),
    url(r'^profile/edit/$', users_views.edit_profile, name='edit_profile'),
    url(r'^profile/(?P<user_id>.*)/$', users_views.other_profile, name='other_profile'),
    url(r'^register/$', users_views.register, name='register'),
    url(r'^scores/$', games_views.last_and_next),
    url(r'^scores/results/$', games_views.full_results, name='full_results'),
    url(r'^scores/fixtures/$', games_views.full_fixtures, name='full_fixtures'),
    url(r'^scores/results/all/$', games_views.results_list, name='list_results'),
    url(r'^scores/fixtures/all/$', games_views.fixture_list, name='list_fixtures'),
    url(r'^scores/(?P<team_name>.*)/$', games_views.games_team, name='team_games'),
    url(r'^standings/$', games_views.league_standings, name='standings'),
    url(r'^teams/$', team_views.team_index),
    url(r'^teams/(?P<team_name>.*)/$', team_views.team_page, name='team_page'),
    url(r'^thread/new/(?P<board_id>\d+)/$', forum_views.new_thread, name='new_thread'),
]
