from __future__ import print_function, unicode_literals
import regex
import argparse
from pyfiglet import Figlet
from prettytable import PrettyTable
from pprint import pprint
from PyInquirer import style_from_dict, Token, prompt
from PyInquirer import Validator, ValidationError
import os
import requests
from pathlib import Path

from . import mangadex
from . import manganelo
from .mangadex import (data,chapter,downloader)
from .manganelo import (data,chapter,downloader)

server={1:manganelo,2:mangadex}

def serv():
	global service
	t=PrettyTable(['Code','Domain','status'])
	try:
		r=requests.get("https://manganelo.tv")
		work="working"
	except:
		work="not working"
	t.add_row([1,'manganelo',work])
	try:
		r=requests.get("https://mangadex.tv")
		work="working"
	except:
		work="not working"
	t.add_row([2,'mangadex',work])
	print(t)
	question=[
	{
		'type': 'input',
		'name': 'server_name',
		'message': 'Select any domain from where you wanna download manga?'
	}]
	keyword=prompt(question, style=style)
	try:
		service=int(keyword.get('server_name'))
	except:
		exit("!!!")



def start():
	global service
	question = [
			{
				'type': 'input',
				'name': 'manga',
				'message': 'Manga you wanna search?'
			}
		]
	keyword = prompt(question, style=style)
	if keyword.get('manga')=="":
		exit()
	else:
		manganame=keyword.get('manga')
		server[service].data.get_data(manganame)

def chapter():
	global service
	question=[
	{
		'type': 'input',
		'name': 'data',
		'message':'Select manga you wanna download using code number?'
	}]
	keyword=prompt(question, style=style)
	if keyword.get('data')=="":
		exit()
	else:
		try:
			url=server[service].data.dic.get(int(keyword.get('data')))
			server[service].chapter.get_chapter(url)
		except:
			exit("!!!")

def select():
	question=[
	{
		'type': 'input',
		'name': 'chapter',
		'message': 'Select chapters you wanna download using code number?'
	}]
	keyword=prompt(question,style=style)
	if keyword.get('chapter')=="":
		exit()
	else:
		try:
			validate(keyword.get('chapter'))
		except:
			exit("!!!")

def validate(ch):
	global chapters
	chapters=[]
	if ch.count('-')==0 and ch.count(',')==0:
		chapters=[[ch,ch]]
	elif ch.count('-')==0 and ch.count(',')>0:
		for i in list(ch.split(',')):
			chapters.append([i,i])
	elif ch.count('-')==1 and ch.count(',')==0:
		chapters.append(list(ch.split('-')))
	elif ch.count('-')>1 and ch.count(',')==0:
		exit("!!! Not the correct format")
	elif ch.count('-')>0 and ch.count(',')>0:
		for i in list(ch.split(',')):
			if '-' not in i:
				s1,s2=i,i
			else:
				s1,s2=i.split('-')
			chapters.append([s1,s2])

def downdir():
	global download_dir
	question=[
	{
		'type':'input',
		'name':'directory',
		'message':'Path to download?'
	}]
	keyword=prompt(question,style=style)
	if keyword.get('directory')=="":
		download_dir=str(os.path.join(Path.home(), "Downloads"))
		download_dir=os.path.normpath(download_dir)
	else:
		download_dir=keyword.get('directory')
		download_dir=os.path.normpath(download_dir)
		if not os.path.exists(download_dir):
			print("Path doesnot exists")
			exit()

def finish():
	global download_dir
	global service
	global chapters
	for i in chapters:
		for j in range(int(i[0]),int(i[1])+1):
			url=server[service].chapter.chapterlink.get(j)
			server[service].downloader.download(url,download_dir)



f = Figlet(font='slant')
print(f.renderText('Re-Manga'))

style = style_from_dict({
	Token.QuestionMark: '#E91E63 bold',
	Token.Selected: '#673AB7 bold',
	Token.Instruction: '',  # default
	Token.Answer: '#2196f3 bold',
	Token.Question: '',
})