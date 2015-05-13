# -*- coding: utf-8 -*-

from django.template import Context, loader
from django.shortcuts import render
from django.core.mail import send_mail
from celery import shared_task
 
# 이메일 인증 키 발송
@shared_task
def send_activationkey(host, user, key):
    
    # 탬플릿 로드하기
    tpl_mail = loader.get_template("mail_form/activate.html")
    
    # 컨텍스트 준비
    ctx_mail = Context()
    
    # 컨텍스트 할당, host 주소와 인증 key
    ctx_mail["host"] = host
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

