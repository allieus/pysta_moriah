# -*- coding: utf-8 -*-

from django.http import HttpResponse
from django.shortcuts import render
from django.template import Context, loader

def dress_gnb(view_func):
	def inner(request, *args, **kwargs):
	
		ctx = Context({
		})
		
		# �� �Լ� ȣ��
		view_ret = view_func(request, *args, **kwargs)
		
		# Ÿ�� Ȯ��
		if (not type(view_ret) is HttpResponse):
			return view_ret
		
		ctx["contents_for_layout"] = view_ret.content
		
		tpl = loader.get_template('gnb/default.html')
		return HttpResponse(tpl.render(ctx))
		
	return inner
