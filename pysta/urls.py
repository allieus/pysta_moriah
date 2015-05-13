# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'pysta.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

	url(r'^member/register', 'member.views.register'),
    url(r'^admin/', include(admin.site.urls)),
)
