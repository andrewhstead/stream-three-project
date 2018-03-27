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
from django.views.static import serve
from .settings import MEDIA_ROOT

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', home_views.home_page),
    url(r'^media/(?P<path>.*)$', serve, {'document_root': MEDIA_ROOT}),
    url(r'^news/$', news_views.news_index),
    url(r'^news/(?P<id>\d+)/$', news_views.news_item),
    url(r'^news/(?P<team_name>.*)/$', news_views.news_team, name='team_news'),
    url(r'^scores/$', games_views.last_and_next),
    url(r'^standings/$', games_views.league_standings),
    url(r'^teams/$', team_views.team_index),
    url(r'^teams/(?P<team_name>.*)/$', team_views.team_page, name='team_page'),
]
