# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'pysta.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

	url(r'^member/register', 'member.views.register'),
	url(r'^member/activate', 'member.views.activate'),
	url(r'^member/issue_activation', 'member.views.issue_activation'),
	url(r'^member/modify', 'member.views.modify'),

	url(r'^member/is_login', 'member.views.is_login'),

	url(r'^member/login', 'member.views.login'),
	url(r'^member/logout$', 'django.contrib.auth.views.logout',{'next_page': '/member/is_login'}, name="logout_url"),

	url(r'^profile$', 'member.views.profile'),
	url(r'^profile/(?P<user_id>[\d]+)$', 'member.views.profile'),
	url(r'^profile/(?P<user_id>[\d]+)/(?P<page>[\d]+)$', 'member.views.profile'),
	
	url(r'^post/(?P<post_id>[\d]+)/like$', 'timeline.views.like'),
	url(r'^post/(?P<post_id>[\d]+)/unlike$', 'timeline.views.unlike'),
	url(r'^post/(?P<post_id>[\d]+)/do_comment$', 'timeline.views.do_comment'),
	
	url(r'^admin/', include(admin.site.urls)),
	
	
)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

