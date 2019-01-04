from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from app import views as app_views

admin.autodiscover()

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    
    #Index page    
    url(r'^app/$|^app/index$', app_views.index, name='index'),

    #Root page
    url(r'^$', app_views.root_index, name='root_index'),

    #Login in page
    url(r'^app/login$', auth_views.LoginView, name='django.contrib.auth.views.LoginView'),

    url(r'^success/$', app_views.success, name='success'),

    #Logout
    url(r'^app/logout/$', auth_views.LogoutView, {'next_page': '../index'}, name='django.contrib.auth.views.LogOutView'),

    #Subscribe
    #url(r'^app/subscribe$', app_views.subscribe, name='subscribe'),

    #Subscribe
    url(r'^app/subscribe_(?P<masked_key>[0-9]+)$', app_views.subscribe, name='subscribe'),

    #Confirm
    url(r'^app/confirm_(?P<masked_key>[0-9]+)$', app_views.confirm, name='confirm'),

    #Cancel
    url(r'^app/cancel$', app_views.cancel, name='cancel'),

    #FAQ
    url(r'^app/faq$', app_views.faq, name='faq'),

    #About
    url(r'^app/about$', app_views.about, name='about'),

    #Terms
    url(r'^app/terms$', app_views.terms, name='terms'),

    #Trash Talk
    url(r'^app/trash_talk$', app_views.trash_talk, name='trash_talk'),

    #Share
    url(r'^app/share$', app_views.share, name='share'),

    #REST framework
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
