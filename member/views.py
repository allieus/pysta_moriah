# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.template import Context, loader
from django.http import HttpResponse, HttpResponseRedirect
from django.core.context_processors import csrf
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth import login as django_login

from member.models import Profile, ActivationKey
from django.core.mail import send_mail
import re

# Create your views here.

def register(request):
	tpl = loader.get_template("member/register.html")
	ctx = Context({
	})
	
	if (request.POST.has_key('username')):
		username = request.POST['username']
		email = request.POST['email']
		password = request.POST['password']
		password2 = request.POST['password2']
		error = False
		ctx['email'] = email
		ctx['username'] = username
		
		if (password != password2):
			ctx["msg_password"] = "두 패스워드가 일치하지 않습니다"
			error = True

		if not re.match("([^@|\s]+@[^@]+\.[^@|\s]+)",email):
			ctx["msg_email"] = "이메일 형식이 틀립니다"
			error = True
		
		if len(username) < 1:
			ctx["msg_username"] = "이름은 꼭 입력 해 주세요"
			error = True
		
		if len(password) < 1:
			ctx["msg_password"] = "비밀번호는 꼭 입력 해 주세요"
			error = True
		
		if (get_user_model().objects.filter(email=email).count() > 0):
			ctx["msg_email"] = "이미 존재하는 이메일 입니다"
			error = True

		if (get_user_model().objects.filter(username=username).count() > 0):
			ctx["msg_username"] = "이미 존재하는 사용자입니다"
			error = True
			
		if (error):
			ctx.update(csrf(request))
			return HttpResponse(tpl.render(ctx))
		
		
		
		user = get_user_model().objects.create_user(username, email, password)
		profile = Profile()
		profile.user = user
		profile.save()
		
		user.is_active = False
		user.save()
		
		key = ActivationKey.gen_key(user)
		
		#mail form
		tpl_mail = loader.get_template("mail_form/activate.html")
		ctx_mail = Context({})
		ctx_mail["host"] = request.META['HTTP_HOST']
		ctx_mail["key"] = key
		
		msg = tpl_mail.render(ctx_mail)
		
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
				return HttpResponseRedirect("/member/issue_activation")
				
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
	
	
def issue_activation(request):
	tpl = loader.get_template("member/issue_activation.html")
	ctx = Context({
	})
	
	if (request.POST.has_key('email')):
		email = request.POST['email']
		users = get_user_model().objects.filter(email=email)
		
		if (users.count() > 0):
			user = users[0]
			key = ActivationKey.gen_key(user)
			
			#mail form
			tpl_mail = loader.get_template("mail_form/activate.html")
			ctx_mail = Context({})
			ctx_mail["host"] = request.META['HTTP_HOST']
			ctx_mail["key"] = key
			
			msg = tpl_mail.render(ctx_mail)
			
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
	