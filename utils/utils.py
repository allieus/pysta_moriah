# -*- coding: utf-8 -*-

from django.http import HttpResponse
from django.shortcuts import render
from django.template import Context, loader
import os
from django.utils.text import slugify
from urllib import quote
from PIL import Image
from django.conf import settings

# ���� ���ε� �ϱ�
def upload(file, path):
    # ���� �̸� �޾ƿ���
    filename = file._name
    
    # fullpath
    file_path = os.path.join(settings.MEDIA_ROOT, path, filename)
    
    # ������ ���� �̸����� ����
    file_path = safe_filename(file_path)
    
    # ���� ����
    fp = open(file_path, "wb")
    for c in file.chunks():
        fp.write(c)
    
    fp.close()
    return os.path.basename(file_path)

# ����� �����
def make_thumb(filename, path, width, height):

    # ��ġ ����
    file_path_org = os.path.join(settings.MEDIA_ROOT, path, filename)
    file_path_to = os.path.join(settings.MEDIA_ROOT, path, "thumbnail", filename)
    
    # ����, �����
    img = Image.open(file_path_org)
    img.thumbnail((width, height))
    
    # �����ϱ�
    img.save(file_path_to)

def safe_filename(filename_org):
	
	# ���, ���ϸ�, Ȯ���� �и�
	filename = os.path.basename(filename_org)
	file_dir = os.path.dirname(filename_org)
	
	pos = filename.rfind(".")
	file_base = filename[:pos]
	file_ext = filename[pos:]
	
	# ���Ϸ� ��� �ȵǴ� ���� ����
	file_base = slugify(file_base)
	
	# ���� ũ��
	len_tot = len(file_base) + len(file_ext)
	
	if (len_tot > 120):	# 120 �� ���� ũ��,
		# �߶� ũ��
		len_overflow = len_tot - 120
		file_base = file_base[:-len_overflow]
	
	postfix = 0
	
	file_base = os.path.join(file_dir, file_base)
	filename = u"{0}_{1}{2}".format(file_base, postfix, file_ext)
	
	while (os.path.isfile(filename)):
		postfix = postfix + 1
		filename = u"{0}_{1}{2}".format(file_base, postfix, file_ext)
	
	return filename
	