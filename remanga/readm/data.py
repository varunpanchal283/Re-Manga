import requests
from bs4 import BeautifulSoup
import re
from prettytable import PrettyTable
dic={}
def issub(string1, string2, m, n):
    # Base Cases
    if m == 0:
        return True
    if n == 0:
        return False
 
    # If last characters of two
    # strings are matching
    if string1[m-1] == string2[n-1]:
        return issub(string1, string2, m-1, n-1)
 
    # If last characters are not matching
    return issub(string1, string2, m, n-1)


def get_data(anime):
	url="https://readm.org/manga-list/"+anime[0]
	r=requests.get(url).text
	soup=BeautifulSoup(r,'html.parser').find_all('div',attrs={'class':'poster poster-xs'})
	"""k=1
				t=PrettyTable(['Code','Manga'])
				for i in soup:
					x=str(i.text).lower()
					if issub(anime,x,len(anime),len(x)):
						dic[k]=i.get('href')
						t.add_row([k,x])
						k=k+1
				"""
	k,t=1,PrettyTable(['Code','Manga'])
	for i in soup:
		zz=BeautifulSoup(str(i),"html.parser")
		l="https://readm.org"+zz.find('a').get("href")
		x=str(zz.find('h2').text).lower()
		if issub(anime,x,len(anime),len(x)):
			dic[k]=l
			t.add_row([k,x])
			k=k+1
	t.align='l'
	print(t)