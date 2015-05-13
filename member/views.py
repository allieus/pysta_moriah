# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.template import Context, loader, RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.core.context_processors import csrf
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth import login as django_login

from member.models import Profile, ActivationKey
from timeline.models import Post
from django.core.mail import send_mail
import re
from django.contrib.auth.decorators import login_required
from utils.decorators import dress_gnb
from utils import utils
from django.conf import settings
import os

# Create your views here.

@dress_gnb
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
		
		filename = ""
		if (request.FILES.has_key("profile_photo")):
			file = request.FILES["profile_photo"]
			filename = file._name
			file_path = os.path.join(settings.MEDIA_ROOT, "profile", filename)
			file_path = utils.safe_filename(file_path)
			filename = os.path.basename(file_path)
			
			fp = open(file_path, "wb")
			
			for c in file.chunks():
				fp.write(c)
			
			fp.close()
			
			from PIL import Image
			img = Image.open(file_path)
			img.thumbnail((100, 100))
			img.save(os.path.join(settings.MEDIA_ROOT, "profile", "thumbnail", filename))
			
			
				
		
		user = get_user_model().objects.create_user(username, email, password)
		profile = Profile()
		profile.user = user
		profile.profile_image = filename
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

@dress_gnb
def is_login(request):
	if (request.user.is_authenticated()):
		return HttpResponse("after login")
	else:
		return HttpResponse("before login")

@dress_gnb
def login(request):
	
	if (request.REQUEST.has_key('next')):
		next  = request.REQUEST["next"]
	else:
		next = "/member/is_login"

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
				return HttpResponseRedirect(next)
			else:
				return HttpResponseRedirect("/member/issue_activation")
				
		else:
			# 로그인 실패 이유를 찾기 위해서 사용자 검색
			if (get_user_model().objects.filter(username=username).exists()):
				ctx["msg_password"] = u"패스워드 에러";
			else:
				ctx["msg_username"] = u"계정 에러";
	
	ctx.update(csrf(request))
	ctx["next"] = next
	return HttpResponse(tpl.render(ctx))

@dress_gnb
def activate(request):
	key = request.GET['key']
	user = ActivationKey.by_key(key)
	if (user == None):
		return HttpResponse(u"invalid key")
	
	user.is_active = True
	user.save()
	return HttpResponse("activated")
	
	
@dress_gnb
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

@dress_gnb
@login_required
def modify(request):
	tpl = loader.get_template("member/modify.html")
	ctx = Context({
	})

	if (request.POST.has_key('email')):
		email = request.POST['email']
		password = request.POST['password']
		password2 = request.POST['password2']
		error = False
		
		if not re.match("([^@|\s]+@[^@]+\.[^@|\s]+)",email):
			ctx["msg_email"] = "이메일 형식이 틀립니다"
			error = True

		if (email != request.user.email and get_user_model().objects.filter(email=email).count() > 0):
			ctx["msg_email"] = "이미 존재하는 이메일 입니다"
			error = True
			
		if len(password) > 0:
			if (password != password2):
				ctx["msg_password"] = "두 패스워드가 일치하지 않습니다"
				error = True

			if (error == False):
				request.user.set_password(password)

		if (request.FILES.has_key("profile_photo")):
			file = request.FILES["profile_photo"]
			filename = file._name
			file_path = os.path.join(settings.MEDIA_ROOT, "profile", filename)
			file_path = utils.safe_filename(file_path)
			filename = os.path.basename(file_path)
			
			fp = open(file_path, "wb")
			
			for c in file.chunks():
				fp.write(c)
			
			fp.close()
			
			from PIL import Image
			img = Image.open(file_path)
			img.thumbnail((100, 100))
			img.save(os.path.join(settings.MEDIA_ROOT, "profile", "thumbnail", filename))
			
			request.user.profile.profile_image = filename
		
		
		if (error):
			ctx.update(csrf(request))
			
			# 기본 값 세팅
			ctx["username"] = request.user.username
			ctx["email"] = email
			return HttpResponse(tpl.render(ctx))
		
		request.user.email = email
		request.user.profile.save()
		request.user.save()
		
	ctx["username"] = request.user.username
	ctx["email"] = request.user.email
	ctx.update(csrf(request))
	
	return HttpResponse(tpl.render(ctx))

	
@dress_gnb
@login_required
def profile(request, user_id=0, page=1):

	# 페이지 사용자 가져오기
	page_owner = None
	
	if (user_id == 0):
		# 사용자 id 가 지정되지 않은 경우, 내 정보 확인
		if not request.user.is_authenticated():
			# 로그인이 안 된 경우 redirect
			return HttpResponseRedirect(settings.LOGIN_URL + "?next=/profile")
		
		# page_owner 에 내 정보 삽입
		page_owner = request.user
	else:
		# todo; 404 처리
		page_owner = get_user_model().objects.get(id=user_id)
		
	tpl = loader.get_template("member/profile.html")
	
	# context -> requestcontext 로 변경
	ctx = RequestContext(request)

	# 내 페이지에서만 업로드 처리
	if (page_owner == request.user and request.FILES.has_key("image")):
		file = request.FILES["image"]
		filename = file._name
		file_path = os.path.join(settings.MEDIA_ROOT, "post", filename)
		file_path = utils.safe_filename(file_path)
		filename = os.path.basename(file_path)
		
		fp = open(file_path, "wb")
		
		for c in file.chunks():
			fp.write(c)
		
		fp.close()
		
		from PIL import Image
		img = Image.open(file_path)
		img.thumbnail((600, 900))
		img.save(os.path.join(settings.MEDIA_ROOT, "post", "thumbnail", filename))
		
		post = Post()
		post.image = filename
		post.contents = request.POST["contents"]
		post.owner = request.user
		post.save()

	#ctx.update(csrf(request))
	
	# 페이지 정보 삽입
	ctx["page_owner"] = page_owner
	ctx["posts"] = page_owner.posts.order_by("-created_at")
	
	return HttpResponse(tpl.render(ctx))
