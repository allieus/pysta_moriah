# -*- coding: utf-8 -*-

from django.http import HttpResponse
from django.shortcuts import render
from django.template import Context, loader
import os
from django.utils.text import slugify
from urllib import quote

def safe_filename(filename_org):
	
	# 경로, 파일명, 확장자 분리
	filename = os.path.basename(filename_org)
	file_dir = os.path.dirname(filename_org)
	
	pos = filename.rfind(".")
	file_base = filename[:pos]
	file_ext = filename[pos:]
	
	# 파일로 허용 안되는 문자 제거
	file_base = slugify(file_base)
	
	# 파일 크기
	len_tot = len(file_base) + len(file_ext)
	
	if (len_tot > 120):	# 120 자 보다 크면,
		# 잘라낼 크기
		len_overflow = len_tot - 120
		file_base = file_base[:-len_overflow]
	
	postfix = 0
	
	file_base = os.path.join(file_dir, file_base)
	filename = u"{0}_{1}{2}".format(file_base, postfix, file_ext)
	
	while (os.path.isfile(filename)):
		postfix = postfix + 1
		filename = u"{0}_{1}{2}".format(file_base, postfix, file_ext)
	
	return filename
	