# -*- coding: utf-8 -*-
import sys
import codecs
sys.stdout = codecs.getwriter('utf8')(sys.stdout)
from django.db import models
from django.conf import settings

# Create your models here.

class Post(models.Model):
    # 포스트 내용
    contents = models.TextField(null=False)
    
    # 이미지 file명
    image = models.CharField(max_length=128)
    
    # 작성자
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="posts")
    
    # 작성일시
    created_at = models.DateTimeField(auto_now_add=True)
    
    # 좋아요 한 사용자
    liked = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="likes")
    
    def image_url_thumb(self):
        return settings.MEDIA_URL + "post/thumbnail/" + self.image

# 댓글
class Comment(models.Model):
    # 댓글 내용
    contents = models.TextField(null=False)
    
    # 작성자
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="comments")
    
    # 글이 속한 post
    post = models.ForeignKey(Post, related_name="comments")
    
    # 작성일시
    created_at = models.DateTimeField(auto_now_add=True)

