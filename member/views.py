# -*- coding: utf-8 -*-

import os

from django.template import Context, loader
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django.contrib.auth import login as django_login
from django.shortcuts import redirect, render
from django.core.paginator import Paginator
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.conf import settings

from utils import utils
from .models import Profile, ActivationKey
from .forms import RegistrationForm, LoginForm, \
        ModificationForm, ActivationForm

# 회원 등록
def register(request):
    tpl = loader.get_template("member/register.html")
    ctx = Context({
    })
    
    # 폼 제출시
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        
        # 입력 값 정상인 경우
        if form.is_valid():
            # 사용자 만들기
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            
            # profile 만들기
            profile = Profile(user=user)
            
            # 프로필 이미지 업로드
            if (request.FILES.has_key("profile_photo")):
                filename = utils.upload(request.FILES["profile_photo"], "profile")
                utils.make_thumb(filename, "profile", 100,100)
                profile.profile_image = filename
            
            # profile 저장
            profile.save()

            # 이메일 인증 키 생성 및 발송
            key = ActivationKey.gen_key(user)
            send_activationkey(request, user, key)

            return redirect('member:login')
    else:
        # 폼 제출 전 (회원 가입 양식 보이기)
        form = RegistrationForm()
        
    return render(request, 'member/register.html', {'form': form})

    
# 로그인 확인
def is_login(request):
    if (request.user.is_authenticated()):
        return HttpResponse("after login")
    else:
        return HttpResponse("before login")

        
# 로그인 처리
def login(request):

    # 폼 제출시
    if request.method == 'POST':
        
        form = LoginForm(data=request.POST)
        # 로그인 성공
        if form.is_valid():
            
            # 세션 세팅
            django_login(request, form.user)
            
            # 기본 페이지로 redirect
            return redirect('member:is_login')
    else:
        form = LoginForm
        
    return render(request, 'member/login.html', {'form': form})
    
    
# 사용자 인증
def activate(request):
    
    key = request.GET['key']
    
    # 인증키로 사용자 가져오기
    user = ActivationKey.by_key(key)
    
    # 해당 키로 사용자를 못 찾은 경우
    if (user == None):
        return HttpResponse(u"invalid key")
    
    # 인증 완료 상태로 바꾸기
    user.is_active = True
    user.save()
    
    return HttpResponse("activated")
    
# 인증키 재 발송
def issue_activation(request):
    
    # 폼 제출시
    if request.method == 'POST':
        form = ActivationForm(request.POST)
        
        if form.is_valid():
            # 이메일 인증 키 생성 및 발송
            key = ActivationKey.gen_key(form.user)
            send_activationkey(request, form.user, key)

            return redirect('member:login')
    else:
        form = ActivationForm()
    
    return render(request, "member/issue_activation.html", {"form":form})
    

# 사용자 정보 수정
@login_required
def modify(request):

    # 폼 제출시
    if request.method == 'POST':
        form = ModificationForm(request.POST, instance=request.user)
        
        # 폼 내용이 정상이면
        if form.is_valid():
        
            # 폼 내용 저장하기
            user = form.save(commit=False)
            user.save()
            
            # 프로필 이미지 업로드, 업로드 된 경우에만
            if (request.FILES.has_key("profile_photo")):
                filename = utils.upload(request.FILES["profile_photo"], "profile")
                utils.make_thumb(filename, "profile", 100,100)
                user.profile.profile_image = filename

            user.profile.save()

    else:
        form = ModificationForm(instance=request.user)
    
    return render(request, "member/modify.html", {"form":form})
    
# 이메일 인증 키 발송
def send_activationkey(request, user, key):
    
    # 탬플릿 로드하기
    tpl_mail = loader.get_template("mail_form/activate.html")
    
    # 컨텍스트 준비
    ctx_mail = Context()
    
    # 컨텍스트 할당, host 주소와 인증 key
    ctx_mail["host"] = request.META['HTTP_HOST']
    ctx_mail["key"] = key
    
    # 렌더링
    msg = tpl_mail.render(ctx_mail)
    
    # 메일 보내기
    send_mail(
            u'인증하여 주십시오', 
            '', 
            u'binseop3@gmail.com',
            [user.email],
            fail_silently=False,
            html_message=msg
    )

