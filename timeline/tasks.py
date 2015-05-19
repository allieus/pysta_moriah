# -*- coding: utf-8 -*-
import sys
import codecs
sys.stdout = codecs.getwriter('utf8')(sys.stdout)

from django.template import Context, loader
from django.shortcuts import render
from django.core.mail import send_mail
from celery import shared_task
 
# post 배송하기 (push timeline)
@shared_task
def distribute(post):
    for follower in post.owner.profile.follower.all():
        # 친구에게 배송하기
        post.reader.add(follower)
    
    # 나에게도 배송하기
    post.reader.add(post.owner)

    
# 지금까지 쓴 글 배송하기
@shared_task
def distribute_on_follow(user_follow, user_follower):
    for post in user_follow.posts.all():
        user_follower.profile.timeline.add(post)
    

# 지금까지 배송된 글 제거하기
@shared_task
def remove_on_unfollow(user_follow, user_follower):
    # 제거할 대상 찾기
    posts_received = user_follower.profile.timeline.filter(owner=user_follow)
    # 제거하기
    user_follower.profile.timeline.remove(*posts_received)
    
