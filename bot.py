#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2019 Atul-Kadian
import time
import requests
import subprocess
import os
import logging
import re
import httplib
import httplib2
import urllib2
import json
import html
import telegram
from functools import wraps
from telegram import InlineKeyboardMarkup, InlineKeyboardButton as Button
from telegram.ext import Updater
from telegram.ext.dispatcher import run_async
from telegram.ext import MessageHandler
from telegram.ext import Filters
from telegram.ext import CommandHandler
from telegram import ChatAction
import validators
import modules.download as download
import modules.download_audio as download_audio
import modules.download_video as download_video
import modules.upload as upload
from modules.text_data import Text
from modules.credentials import Creds

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

size = "empty"
filename="none"
TOKEN = Creds.TOKEN
ADMIN_MODULE = True
try:
	import private.extra_funcs as extras
except ImportError:
	ADMIN_MODULE = False

@run_async
def start(bot,update):
	bot.send_message(chat_id=update.message.chat_id, text=Text.GREET_USER.format(update.message.from_user.first_name))

@run_async
def help(bot,update):
	bot.send_message(chat_id=update.message.chat_id, text=Text.HELP, parse_mode=telegram.ParseMode.HTML)

@run_async
def donate(bot,update):
	keyboard = [[telegram.InlineKeyboardButton("PayPal", url="www.paypal.me/AtulKadian")],
		[telegram.InlineKeyboardButton("PayTM", url="https://telegra.ph/Like-my-work--Buy-me-some-snacks-01-25")]]
	reply_markup = telegram.InlineKeyboardMarkup(keyboard)
	update.message.reply_text(Text.DONATE, reply_markup=reply_markup)


@run_async
def start_bot(bot, update):
	msg=update.message.text
	msg=str(msg)
	user_id=update.message.from_user.id
	user_id =str(user_id)
	if "|" in msg:
		user_cmd, url = msg.split("|")
		user_cmd = user_cmd.strip()
		user_cmd = user_cmd.lower()
		url = url.strip()
	else:
		user_cmd = None
		url = msg
	#site = requests.get(url)
	#if site.status_code == 200:
	#site = httplib.HTTPConnection(url)
	#site.request("HEAD", '')
	#if site.getresponse().status == 200:
	sent_message = bot.send_message(chat_id=update.message.chat_id, text=Text.VERIFYING_URL)
	time.sleep(1)
	if validators.url(url):
		sent_message.edit_text(Text.PROCESSING)
		if user_cmd:
			if(user_cmd == "video"):
				filename = download_video.download(url)
				if "ERROR" in filename:
					sent_message.edit_text(Text.FAILED+filename, parse_mode=telegram.ParseMode.HTML)
				else:
					bot.send_chat_action(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
					sent_message.edit_text(Text.UPLOADING_GD)
					dwnld_url = upload.upload(filename)
					size = (os.path.getsize(filename))/1048576
					sent_message.edit_text(Text.DONE.format(filename, size, dwnld_url),parse_mode=telegram.ParseMode.HTML)
					os.remove(filename)
			elif(user_cmd == "audio"):
				if("youtube" in url or "youtu" in url):
					filename = download_audio.download(url)
					if "ERROR" in filename:
						sent_message.edit_text(Text.FAILED+filename, parse_mode=telegram.ParseMode.HTML)
					else:
						bot.send_chat_action(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
						sent_message.edit_text(Text.UPLOADING_TG)
						audio=open(filename, 'rb')
						bot.send_audio(chat_id=update.message.chat_id, audio=audio, caption=filename.replace(".mp3",""))
						audio.close()
						os.remove(filename)
						sent_message.edit_text(Text.DONE)
				else:
					sent_message.edit_text(Text.NOT_SUPPORTED,parse_mode=telegram.ParseMode.HTML)
			else:
				if download.is_downloadable(url):
					size = download.check_filesize(url)
					if size <= 10000:
						filename = user_cmd
						raw_file = download.download(url, filename)
						if "ERROR" in raw_file:
							sent_message.edit_text(Text.FAILED+raw_file, parse_mode=telegram.ParseMode.HTML)
						else:
							bot.send_chat_action(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
							sent_message.edit_text(Text.UPLOADING_GD)
							dwnld_url = upload.upload(raw_file)
							sent_message.edit_text(Text.DONE.format(raw_file, size, dwnld_url),parse_mode=telegram.ParseMode.HTML)
							os.remove(raw_file)
					else:
						sent_message.edit_text(Text.MAXLIMITEXCEEDED)
				else:
					sent_message.edit_text(Text.ISNOT_DOWNLOADABLE,parse_mode=telegram.ParseMode.HTML)
		else:
			if download.is_downloadable(url):
				size = download.check_filesize(url)/1048576
				if size <= 10000:
					raw_file = download.download(url, None)
					bot.send_chat_action(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
					sent_message.edit_text(Text.UPLOADING_GD)
					dwnld_url = upload.upload(raw_file)
					sent_message.edit_text(Text.DONE.format(raw_file, size, dwnld_url),parse_mode=telegram.ParseMode.HTML)
			 		os.remove(raw_file)
				else:
					sent_message.edit_text(Text.MAXLIMITEXCEEDED)
			else:
				sent_message.edit_text(Text.ISNOT_DOWNLOADABLE,parse_mode=telegram.ParseMode.HTML)
	elif("help" not in url and "start" not in url and "broadcast" not in url and "donate" not in url and "add_user" not in url and "revoke_user" not in url):
		bot.send_chat_action(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
		time.sleep(1)
		sent_message.edit_text(Text.RETARD)

def main():
	updater = Updater(token=TOKEN, workers = 8)
	dispatcher = updater.dispatcher
	start_cmd = CommandHandler("start" , start)
	help_cmd = CommandHandler("help" , help)
	donate_cmd = CommandHandler("donate" , donate)
	dispatcher.add_handler(start_cmd)
	dispatcher.add_handler(help_cmd)
	dispatcher.add_handler(donate_cmd)
	if ADMIN_MODULE:
		extras.add_extra_commands(dispatcher)
	else:
		print("ADMIN_MODULE not found. (Won't effect the bot though.)")
		start_handler = MessageHandler((Filters.all) , start_bot)
		dispatcher.add_handler(start_handler)
	updater.start_polling()

if __name__ == '__main__':
    main()
