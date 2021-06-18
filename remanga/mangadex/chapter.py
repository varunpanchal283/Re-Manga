import requests
from bs4 import BeautifulSoup
from prettytable import PrettyTable

chapterlink={}
chaptername={}

def get_chapter(url):
	r=requests.get(url).text
	soup=BeautifulSoup(r,'html.parser').find('div',attrs={'class':'chapter-container'}).find_all('a',attrs={'class':'text-truncate'})
	t=PrettyTable(['Code','Chapter-Name'])
	arr=[]
	k=1
	"""for i in soup:
					link="https://mangadex.tv/"+i.get('href')
					t.add_row([k,i.text])
					chapterlink[k]=link
					k+=1
				print(t)
			"""
	for i in soup:
		link="https://mangadex.tv/"+i.get('href')
		arr.append((link,i.text))
	dat=arr[::-1]
	for (link,chapter) in dat:
		t.add_row([k,chapter])
		chapterlink[k]=link
		chaptername[k]=chapter
		k+=1
	t.align='l'
	print(t)