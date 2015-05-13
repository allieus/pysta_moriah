# -*- coding: utf-8 -*-
from django.shortcuts import render
from timeline.models import Post, Comment
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

def do_comment(request, post_id):

	# post 찾기
	p = Post.objects.get(id=post_id)
	
	# 글 작성하기
	cmt_obj = Comment()
	cmt_obj.contents = request.POST["contents"]	# 글 내용
	cmt_obj.owner = request.user	# 작성자 assign
	cmt_obj.post = p	# 글 assign
	cmt_obj.save()
	
	# profile page 로 redirect
	return HttpResponseRedirect(request.POST["next"])

