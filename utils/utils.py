# -*- coding: utf-8 -*-

from django.http import HttpResponse
from django.shortcuts import render
from django.template import Context, loader
import os
from django.utils.encoding import smart_bytes

def safe_filename(filename):
	fn_bytes = smart_bytes(filename)
	fn_bytes = fn_bytes.replace("\\x", "")
	fn_bytes = fn_bytes.replace(" ", "_")
	
	pos = fn_bytes.rfind(".")
	fn_base = fn_bytes[:pos]
	fn_ext = fn_bytes[pos:]

	if (len(fn_bytes) > 120):
		fn_base = fn_base[:115]
	
	postfix = 0
	
	while (os.path.isfile(fn_bytes)):
		postfix = postfix + 1
		fn_bytes = "{0}_{1}{2}".format(fn_base,postfix,fn_ext)
	
	return fn_bytes
	