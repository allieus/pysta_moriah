# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'pysta.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

	url(r'^member/register', 'member.views.register'),

	url(r'^member/is_login', 'member.views.is_login'),

	url(r'^member/login', 'member.views.login'),
	url(r'^member/logout$', 'django.contrib.auth.views.logout',{'next_page': '/member/is_login'}, name="logout_url"),

	url(r'^admin/', include(admin.site.urls)),
	
	
)
