import requests
from bs4 import BeautifulSoup as bs
from prettytable import PrettyTable

chapterlink={}
chaptername={}

def get_chapter(url):
	r=requests.get(url).text
	soup=bs(r,'html.parser').find('ul',attrs={'class':'chapter-list'}).find_all('a')
	t=PrettyTable(['Code','Chapter-Name'])
	name,link=[],[]
	k=1
	for i in soup:
		name.append(bs(str(i),'html.parser').find('span',attrs={'class':'val'}).text)
		link.append(i.get('href'))
	name=name[::-1]
	link=link[::-1]
	for i in range(len(name)):
		chapterlink[i+1]=link[i]
		chaptername[i+1]=name[i]
		t.add_row([i+1,name[i]])
	t.align='l'
	print(t)