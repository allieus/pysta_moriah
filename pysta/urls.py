# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings

# member urls
urls_member = patterns('',

    # register/modify
    url(r'^register/$', 'member.views.register', name="register"),
    url(r'^modify/$', 'member.views.modify', name="modify"),
    
    # login/out
    url(r'^login/$', 'member.views.login', name="login"),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/member/is_login'}, name="logout_url"),

    # activation
    url(r'^activate/$', 'member.views.activate', name="activate"),
    url(r'^issue_activation/$', 'member.views.issue_activation', name="issue_activation"),
    
    # temporary
    url(r'^is_login/$', 'member.views.is_login', name="is_login"),
)

# profile urls
urls_profile = patterns('',
    # profile main
    url(r'^$', 'timeline.views.profile', name="profile"),
    url(r'^(?P<user_id>[\d]+)/$', 'timeline.views.profile', name="profile"),
    url(r'^(?P<user_id>[\d]+)/(?P<page>[\d]+)/$', 'timeline.views.profile', name="profile"),
    
    # followers/followings
    url(r'^(?P<user_id>[\d]+)/followers$', 'timeline.views.followers', name="followers"),
)

# timeline urls
urls_timeline = patterns('',
    # post action
    url(r'^post/create/$', 'timeline.views.post', name="create"),
    url(r'^post/(?P<post_id>[\d]+)/like/$', 'timeline.views.like', name="like"),
    url(r'^post/(?P<post_id>[\d]+)/unlike/$', 'timeline.views.unlike', name="unlike"),
    url(r'^post/(?P<post_id>[\d]+)/do_comment/$', 'timeline.views.do_comment', name="do_comment"),
    url(r'^post/(?P<comment_id>[\d]+)/remove_comment/$', 'timeline.views.remove_comment', name="remove_comment"),

    # follow/unfollow
    url(r'^follow/(?P<user_id>[\d]+)/$', 'timeline.views.follow', name='follow'),
    url(r'^unfollow/(?P<user_id>[\d]+)/$', 'timeline.views.unfollow', name='unfollow'),
)

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^member/', include(urls_member, namespace='member')),
    url(r'^profile/', include(urls_profile, namespace='profile')),
    url(r'^timeline/', include(urls_timeline, namespace='timeline')),
)



urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

