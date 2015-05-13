# -*- coding: utf-8 -*-
from django.db import models
from django.conf import settings

# Create your models here.

class Post(models.Model):
	# 포스트 내용
	contents = models.TextField(null=False)
	
	# 이미지 file명
	image = models.TextField()
	
	# 작성자
	owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="posts")
	
	# 작성일시
	created_at = models.DateTimeField(auto_now_add=True)

	def image_url_thumb(self):
		return settings.MEDIA_URL + "post/thumbnail/" + self.image
		