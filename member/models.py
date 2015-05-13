# -*- coding: utf-8 -*-
from django.db import models
from django.conf import settings
import random, string

# Profile model
class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    profile_image = models.CharField(max_length=128)
    
    def profile_image_url_thumb(self):
        return settings.MEDIA_URL + "profile/thumbnail/" + self.profile_image
    
# activation key
class ActivationKey(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    activation_key = models.CharField(max_length=64, unique=True)
    
    # 키 생성
    @staticmethod
    def gen_key(user):
    
        key = ""
        for i in range(0,64):
            key = key + random.choice(string.ascii_letters + string.digits)
        
        if (ActivationKey.objects.filter(activation_key=key).count() != 0):
            return gen_key
        
        key_obj = ActivationKey(user=user, activation_key=key)
        key_obj.save()
        
        return key;

    # 키로 사용자 찾기
    @staticmethod
    def by_key(key):
        keys = ActivationKey.objects.filter(activation_key=key)
        
        if (keys.count() > 0):
            return keys[0].user

        return None
        
        