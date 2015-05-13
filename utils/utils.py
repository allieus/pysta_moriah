# -*- coding: utf-8 -*-

from django.http import HttpResponse
from django.shortcuts import render
from django.template import Context, loader
import os
from django.utils.text import slugify
from urllib import quote

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
	