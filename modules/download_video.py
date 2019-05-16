#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2019 Atul-Kadian

from __future__ import unicode_literals
import youtube_dl
from pytube import YouTube
import os
import re
def download(url):
	class MyLogger(object):
	    def debug(self, msg):
	        pass

	    def warning(self, msg):
	        pass

	    def error(self, msg):
	        print(msg)

	def my_hook(d):
	    if d['status'] == 'finished':
	        print('Done downloading')
	extract_filename = {}
	with youtube_dl.YoutubeDL(extract_filename) as ydl:
		info_dict = ydl.extract_info(url, download=False)
      		video_url = info_dict.get("url", None)
      		video_id = info_dict.get("id", None)
      		video_title = info_dict.get('title', None)
		video_extension = str(info_dict.get('ext', None))
		filename = str(video_title)
		filename = re.sub(r'\[\(\)\{\}\<\>\-\|\]', '', filename)
                filename = re.sub(r'\[\[(?:[^|\]]*\|)?([^\]]*)]]', r'\1', filename)
		filename = filename.replace("|", "")
		filename = filename.strip()
		filename = filename+"."+video_extension

	if("youtube" in url or "youtube" in url):
		ydl_opts = {
		'format': 'bestvideo[height<=1080]',
		'outtmpl': unicode(filename),
	    	'logger': MyLogger(),
		'progress_hooks': [my_hook],
	}
	else:
		ydl_opts = {
		'outtmpl': unicode(filename),
	    	'logger': MyLogger(),
		'progress_hooks': [my_hook],
	}
	try:
		with youtube_dl.YoutubeDL(ydl_opts) as ydl:
			ydl.download([url])
	except Exception as e:
		print(e)
		ERROR = "ERROR CODE-2b-1"
		return ERROR
	print("RETURNED : ", filename)
	return filename
