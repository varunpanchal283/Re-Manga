import requests
from bs4 import BeautifulSoup
import re
from prettytable import PrettyTable
dic={}

def get_data(anime):
	for i in anime:
		if i==" ":
			anime=anime.replace(" ","+")
	url="https://manganelo.tv/search/"+anime
	r=requests.get(url).text
	soup=BeautifulSoup(r,"html.parser").find('div',attrs={'class':'group-page'}).find_all('a')
	for i in soup:
		if "Last" in i.text:
			temp_count=i.text
	pagecount=re.search("\((.*)\)",temp_count).group()[1:-1]
	t=PrettyTable(['Code','Manga'])
	k=1
	for i in range(1,int(pagecount)+1):
		url="https://manganelo.tv/search/"+anime+"?page="+str(i)
		r=requests.get(url).text
		soup=BeautifulSoup(r,"html.parser").find('div',attrs={'class':'panel-search-story'}).find_all('a',attrs={'class':'item-img'})
		for i in soup:
			dic[k]="https://manganelo.tv"+i.get('href')
			t.add_row([k,i.get('title')])
			k=k+1
	print(t)
