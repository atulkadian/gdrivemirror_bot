#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2019 Atul-Kadian

from __future__ import unicode_literals
import youtube_dl
import requests
import urllib2
from urllib import urlretrieve
from pytube import YouTube
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
	        print('Done downloading, now converting ...')

	extract_filename = {}
	#try:
	with youtube_dl.YoutubeDL(extract_filename) as ydl:
		info_dict = ydl.extract_info(url, download=False)
      		video_url = info_dict.get("url", None)
      		video_id = info_dict.get("id", None)
      		video_title = info_dict.get('title', None)
		video_thumb_link = info_dict.get('thumbnail', None)
		filename = str(video_title)
		filename = re.sub(r'\[\(\)\{\}\<\>\-\|\]', '', filename)
                filename = re.sub(r'\[\[(?:[^|\]]*\|)?([^\]]*)]]', r'\1', filename)
		filename = filename.replace("|", "")
		filename = filename.strip()
		#urlretrieve(video_thumb_link, filename+".jpg")
		filename = filename+".mp3"
		filename = filename.strip()

	"""except Exception as e:
		print(e)
		ERROR = "ERROR CODE-2b-1"""

	ydl_opts = {
	    	'format': 'bestaudio/best',
		'outtmpl': unicode(filename),
	    	'postprocessors': [{
	        	'key': 'FFmpegExtractAudio',
	        	'preferredcodec': 'mp3',
	        	'preferredquality': '192'
	    }],
	    'logger': MyLogger(),
	    'progress_hooks': [my_hook],
	}
	try:
		with youtube_dl.YoutubeDL(ydl_opts) as ydl:
			ydl.download([url])
	except Exception as e:
		print(e)
		ERROR = "ERROR CODE-2b-2"
		return ERROR

	return filename
