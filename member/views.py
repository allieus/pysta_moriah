# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.template import Context, loader
from django.http import HttpResponse, HttpResponseRedirect
from django.core.context_processors import csrf
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth import login as django_login

from member.models import Profile, ActivationKey
from django.core.mail import send_mail

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
		
		user.is_active = False
		user.save()
		
		key = ActivationKey.gen_key(user)
		msg = u"<a href=\"http://{host}/member/activate?key={key}\">인증하기</a>".format(host=request.META['HTTP_HOST'], key=key)
				
		send_mail(
				u'인증하여 주십시오', 
				'', 
				u'binseop3@gmail.com',
				[email],
				fail_silently=False,
				html_message=msg
		)

		
	
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
			if (user.is_active):
				# success
				django_login(request, user)
				return HttpResponseRedirect("/member/is_login")
		else:
			# fail
			pass
	
	ctx.update(csrf(request))
	
	return HttpResponse(tpl.render(ctx))

def activate(request):
	key = request.GET['key']
	user = ActivationKey.by_key(key)
	if (user == None):
		return HttpResponse(u"invalid key")
	
	user.is_active = True
	user.save()
	return HttpResponse("activated")
	
	
	
	