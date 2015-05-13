# -*- coding: utf-8 -*-
from django import forms
from django.forms.widgets import Textarea, TextInput
from .models import Post, Comment

# 글 쓰기 Form
class PostingForm(forms.ModelForm):
    photo = forms.FileField(required=False)
    
    class Meta:
        model = Post
        fields = ('contents', )

# 댓글 폼
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('contents', )
        widgets = {
            'contents': TextInput(),
        }
        labels = {
            'contents': 'Comment',
        }
