# -*- coding: utf-8 -*-
from django.shortcuts import render
from timeline.models import Post
from django.http import HttpResponseRedirect

# Create your views here.

def like(request, post_id):

	# post 찾기
	p = Post.objects.get(id=post_id)
	
	# 좋아요 한 사용자 추가하기
	p.liked.add(request.user)
	
	# profile page 로 redirect
	return HttpResponseRedirect(request.GET["next"])

# 좋아요 취소
def unlike(request, post_id):

	# post 찾기
	p = Post.objects.get(id=post_id)
	
	# 좋아요 한 사용자 삭제하기
	p.liked.remove(request.user)
	
	# profile page 로 redirect
	return HttpResponseRedirect(request.GET["next"])

	