# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.template import Context, loader
from django.http import HttpResponse, HttpResponseRedirect
from django.core.context_processors import csrf
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth import login as django_login

from member.models import Profile

# Create your views here.

def register(request):
	tpl = loader.get_template("member/register.html")
	ctx = Context({
	})
	
	if (request.POST.has_key('username')):
		username = request.POST['username']
		email = request.POST['email']
		password = request.POST['password']
		user = get_user_model().objects.create_user(username, email, password)
		profile = Profile()
		profile.user = user
		profile.save()
		user.save()
		
	
	ctx.update(csrf(request))
	
	return HttpResponse(tpl.render(ctx))

def is_login(request):
	if (request.user.is_authenticated()):
		return HttpResponse("after login")
	else:
		return HttpResponse("before login")

def login(request):
	tpl = loader.get_template("member/login.html")
	ctx = Context({
	})
	
	if (request.POST.has_key('username')):
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=username, password=password)
		
		if (user != None):
			# success
			django_login(request, user)
			return HttpResponseRedirect("/member/is_login")
		else:
			# fail
			pass
	
	ctx.update(csrf(request))
	
	return HttpResponse(tpl.render(ctx))
	
	