import requests
from bs4 import BeautifulSoup
from prettytable import PrettyTable

chapterlink={}

def get_chapter(url):
	r=requests.get(url).text
	soup=BeautifulSoup(r,'html.parser').find('ul',attrs={'class':'row-content-chapter'}).find_all('a',attrs={'class':'chapter-name text-nowrap'})
	t=PrettyTable(['Code','Chapter-Name'])
	arr=[]
	k=1
	"""for i in soup:
					link="https://manganelo.tv/"+i.get('href')
					t.add_row([k,i.get('title')])
					chapterlink[k]=link
					k+=1
				print(t)
			"""
	for i in soup:
		link="https://manganelo.tv/"+i.get('href')
		arr.append((link,i.get('title')))
	dat=arr[::-1]
	for (link,chapter) in dat:
		t.add_row([k,chapter])
		chapterlink[k]=link
		if ".5" in chapter:
			k=k+0.5
		else:
			k+=1
	print(t)