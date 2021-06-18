from __future__ import print_function, unicode_literals
import regex
import argparse
from pyfiglet import Figlet
from prettytable import PrettyTable
from pprint import pprint
from PyInquirer import style_from_dict, Token, prompt
from PyInquirer import Validator, ValidationError
import os
import click
import requests
from pathlib import Path
from configparser import ConfigParser 

from . import mangadex
from . import manganelo
from . import funmanga
from .mangadex import (data,chapter,downloader)
from .manganelo import (data,chapter,downloader)
from .funmanga import (data,chapter,downloader)

server={1:funmanga,2:manganelo,3:mangadex}

def url_validate(url):
	global service
	if "mangadex" in url:
		service=3
	elif "manganelo" in url:
		service=2
	else:
		exit("invalid url\
			 Supported Websites are 1: Mangadex.tv\n2. Manganelo.tv\n")

def down_dir(directory):
	if directory=="":
		download_dir=str(os.path.join(Path.home(), "Downloads"))
		download_dir=os.path.normpath(download_dir)
	else:
		download_dir=directory
		download_dir=os.path.normpath(download_dir)
		if not os.path.exists(download_dir):
			print("Path doesnot exists")
			exit()
	return download_dir


def parse():
	global service
	global downdir
	loc=click.get_app_dir('remanga')
	if not os.path.exists(loc):
		os.makedirs(loc)
	downdir= [str(os.path.join(Path.home(), "Downloads"))]
	if "/" in downdir:
		file = loc+"/config.ini"
	else:
		file=loc+"\\config.ini"
	if not os.path.exists(file):
		with open(file, 'w') as f:
			f.write("[download_directory]\n")
			f.write("directory = ")
	config=ConfigParser()
	config.read(file)
	if config.get('download_directory','directory')!="":
		downdir=[config.get('download_directory','directory')]
	parser=argparse.ArgumentParser(prog="re-manga",description="Manga Downloader")
	parser.add_argument('-download','-d',dest="download",nargs=1,type=str,help="will download anime")
	parser.add_argument('-dir',dest="directory",nargs=1,type=str,help="Download directory",default=downdir)
	parser.add_argument('-fn',dest="filename",nargs=1,type=str,help="File Name")
	parser.add_argument('-changedir',dest="downloaddir",nargs=1,type=str,help="Change default download directory")
	args=parser.parse_args()
	if args.download:
		url_validate(args.download[0])
		down_dir(args.directory[0])
		if "chapter" in args.download[0]:
			if args.filename:
				server[service].downloader.download(args.download[0],down_dir(args.directory[0]),args.filename[0])
			else:
				exit("please enter file name!!!")
		else:
			server[service].chapter.get_chapter(args.download[0])
			print("The above chapters will be downloaded")
			x=server[service].chapter.chapterlink
			for i in x:
				server[service].downloader.download(x[i],down_dir(args.directory[0]),server[service].chapter.chaptername[i])
		exit("Enjoy;)")

	elif args.downloaddir:
		temp_dir=down_dir(args.downloaddir[0])
		config.set('download_directory','directory',temp_dir)
		with open(file, 'w') as configfile:
			config.write(configfile)
		exit("The Default download directory has changed to "+temp_dir)


def serv():
	global service
	t=PrettyTable(['Code','Domain','status'])
	try:
		r=requests.get("https://funmanga.com")
		work="working"
	except:
		work="not working"
	t.add_row([1,'funmanga',work])
	try:
		r=requests.get("https://manganelo.tv")
		work="working"
	except:
		work="not working"
	t.add_row([2,'manganelo',work])
	try:
		r=requests.get("https://mangadex.tv")
		work="working"
	except:
		work="not working"
	t.add_row([3,'mangadex',work])
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
	global downdir
	question=[
	{
		'type':'input',
		'name':'directory',
		'message':'Path to download?'
	}]
	keyword=prompt(question,style=style)
	if keyword.get('directory')=="":
		download_dir=downdir[0]
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
			filename=server[service].chapter.chaptername.get(j)
			server[service].downloader.download(url,download_dir,filename)



f = Figlet(font='slant')
print(f.renderText('Re-Manga'))

style = style_from_dict({
	Token.QuestionMark: '#E91E63 bold',
	Token.Selected: '#673AB7 bold',
	Token.Instruction: '',  # default
	Token.Answer: '#2196f3 bold',
	Token.Question: '',
})