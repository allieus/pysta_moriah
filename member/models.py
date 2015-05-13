# -*- coding: utf-8 -*-
from django.db import models
from django.conf import settings
import random, string

# Create your models here.
class Profile(models.Model):
	user = models.OneToOneField(settings.AUTH_USER_MODEL)
	profile_image = models.CharField(max_length=128)

class ActivationKey(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL)
	activation_key = models.CharField(max_length=64, unique=True)
	
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

	@staticmethod
	def by_key(key):
		keys = ActivationKey.objects.filter(activation_key=key)
		
		if (keys.count() > 0):
			return keys[0].user

		return None
		
		