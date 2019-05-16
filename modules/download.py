#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2019 Atul-Kadian

import requests
import subprocess
import os
import logging
import re
import urllib2
import wget
import os.path
def download(url, filename):
	try:
		"""result = urllib2.urlopen(url)
		name = os.path.basename(urllib2.urlparse.urlparse(result.url).path)
                filename = re.sub('[(){}<>-]', '', name)
                filename = re.sub(r'\[\[(?:[^|\]]*\|)?([^\]]*)]]', r'\1', filename)
		downloader = Downloader(url, filename, 5)
		downloader.start()
		downloader.subscribe(callback, callback_threshold)
		downloader.wait_for_finish()"""
		if filename:
			cmd_output = subprocess.check_output('wget -O {} {}'.format(filename, url), stderr=subprocess.STDOUT, shell=True)
		else:
			cmd_output = subprocess.check_output('wget {}'.format(url), stderr=subprocess.STDOUT, shell=True)
		raw_filename = re.findall(r' - ‘(.*?)’ saved', cmd_output)
		filename = str(raw_filename[0])
      	except Exception as e:
		print(e)
		ERROR = "ERROR CODE-a1"
		return ERROR

	return filename

