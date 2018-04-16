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
from store import views as store_views
from forum import views as forum_views
from users import views as users_views
from django.views.static import serve
from .settings import MEDIA_ROOT

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', home_views.home_page),
    url(r'^archive/$', games_views.season_archive, name='archive'),
    url(r'^archive/(?P<year>\d+)/$', games_views.season_overview, name='season_overview'),
    url(r'^archive/(?P<year>\d+)/(?P<team_name>.*)/$', games_views.season_team, name='season_team'),
    url(r'^blogs/$', news_views.blog_home, name='blog_home'),
    url(r'^blogs/post/(?P<post_id>\d+)/$', news_views.blog_post, name='blog_post'),
    url(r'^blogs/post/delete/(?P<post_id>\d+)/$', news_views.delete_blog, name='delete_blog'),
    url(r'^blogs/post/edit/(?P<post_id>\d+)/$', news_views.edit_blog, name='edit_blog'),
    url(r'^blogs/post/new/$', news_views.new_blog_post, name='new_blog_post'),
    url(r'^blogs/user/(?P<author_name>.*)/$', news_views.blog_index, name='blog_index'),
    url(r'^comment/new/(?P<item_id>\d+)/$', news_views.new_comment, name='new_comment'),
    url(r'^comment/edit/(?P<item_id>\d+)/(?P<comment_id>\d+)/$',
        news_views.edit_comment, name='edit_comment'),
    url(r'^comment/delete/(?P<item_id>\d+)/(?P<comment_id>\d+)/$',
        news_views.delete_comment, name='delete_comment'),
    url(r'^forum/$', forum_views.forum_home, name='forum'),
    url(r'^forum/league/(?P<board_id>\d+)/$', forum_views.forum_league, name='forum_league'),
    url(r'^forum/(?P<team_name>.*)/$', forum_views.forum_team, name='forum_team'),
    url(r'^login/$', users_views.login, name="login"),
    url(r'^logout/$', users_views.logout, name="logout"),
    url(r'^media/(?P<path>.*)$', serve, {'document_root': MEDIA_ROOT}),
    url(r'^news/$', news_views.news_index, name='news_index'),
    url(r'^news/(?P<news_id>\d+)/$', news_views.news_item, name='news'),
    url(r'^news/(?P<team_name>.*)/$', news_views.news_team, name='team_news'),
    url(r'^post/new/(?P<thread_id>\d+)/$', forum_views.new_post, name='new_post'),
    url(r'^post/edit/(?P<thread_id>\d+)/(?P<post_id>\d+)/$',
        forum_views.edit_post, name='edit_post'),
    url(r'^post/delete/(?P<thread_id>\d+)/(?P<post_id>\d+)/$',
        forum_views.delete_post, name='delete_post'),
    url(r'^premium/$', store_views.premium_home, name='premium_home'),
    url(r'^premium/cancel/$', store_views.cancel_subscription, name='cancel_subscription'),
    url(r'^premium/renewal/$', store_views.subscription_renewal, name='subscription_renewal'),
    url(r'^premium/upgrade/$', store_views.upgrade_account, name='upgrade'),
    url(r'^profile/$', users_views.user_profile, name='user_profile'),
    url(r'^profile/delete/$', users_views.delete_profile, name='delete_profile'),
    url(r'^profile/edit/$', users_views.edit_profile, name='edit_profile'),
    url(r'^profile/password/$', users_views.change_password, name='change_password'),
    url(r'^profile/(?P<user_id>.*)/$', users_views.other_profile, name='other_profile'),
    url(r'^register/$', users_views.register, name='register'),
    url(r'^register/premium/$', store_views.register_premium, name='register_premium'),
    url(r'^scores/$', games_views.last_and_next, name='score_index'),
    url(r'^scores/results/$', games_views.full_results, name='full_results'),
    url(r'^scores/fixtures/$', games_views.full_fixtures, name='full_fixtures'),
    url(r'^scores/results/all/$', games_views.results_list, name='list_results'),
    url(r'^scores/fixtures/all/$', games_views.fixture_list, name='list_fixtures'),
    url(r'^scores/(?P<team_name>.*)/$', games_views.games_team, name='team_games'),
    url(r'^standings/$', games_views.league_standings, name='standings'),
    url(r'^store/$', store_views.store_front, name='store_front'),
    url(r'^store/cart/$', store_views.shopping_cart, name='shopping_cart'),
    url(r'^store/cart/edit/(?P<item_id>\d+)/$', store_views.change_product, name='change_product'),
    url(r'^store/cart/remove/(?P<item_id>\d+)/$', store_views.remove_product, name='remove_product'),
    url(r'^store/checkout/(?P<order_id>\d+)/$', store_views.submit_order, name='checkout'),
    url(r'^store/confirmation/$', store_views.order_confirmation, name='order_confirmation'),
    url(r'^store/orders/$', store_views.order_list, name='order_list'),
    url(r'^store/order/(?P<order_id>\d+)/$', store_views.order_details, name='order_details'),
    url(r'^store/product/(?P<product_id>\d+)/$', store_views.add_product, name='add_product'),
    url(r'^store/(?P<team_name>.*)/$', store_views.store_team, name='store_team'),
    url(r'^teams/$', team_views.team_index, name='team_index'),
    url(r'^teams/(?P<team_name>.*)/$', team_views.team_page, name='team_page'),
    url(r'^thread/new/(?P<board_id>\d+)/$', forum_views.new_thread, name='new_thread'),
    url(r'^thread/(?P<thread_id>\d+)/$', forum_views.view_thread, name='view_thread'),
]
