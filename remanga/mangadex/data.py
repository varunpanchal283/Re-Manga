import requests
from bs4 import BeautifulSoup
import re
from prettytable import PrettyTable
dic={}

def get_data(anime):
	for i in anime:
		if i==" ":
			anime=anime.replace(" ","+")
	url="https://mangadex.tv/search?type=titles&title="+anime
	r=requests.get(url).text
	soup=BeautifulSoup(r,"html.parser").find_all('a',attrs={'class':'page-link'})
	for i in soup:
		if "Last" in i.text:
			temp_count=i.text
	pagecount=re.search("\((.*)\)",temp_count).group()[1:-1]
	t=PrettyTable(['Code','Manga'])
	k=1
	for i in range(1,int(pagecount)+1):
		url="https://mangadex.tv/search?type=titles&title="+anime+"&page="+str(i)
		r=requests.get(url).text
		soup=BeautifulSoup(r,"html.parser").find_all('a',attrs={'class':'ml-1 manga_title text-truncate'})
		for i in soup:
			dic[k]="https://mangadex.tv"+i.get('href')
			t.add_row([k,i.text])
			k=k+1
	t.align='l'
	print(t)
