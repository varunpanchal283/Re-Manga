import requests
import os
from bs4 import BeautifulSoup
import img2pdf
import shutil
import time
import re
import threading
import sys

def progress():
	global x
	i=0
	animation = "|/-\\"
	while x==0:
		sys.stdout.write("\rDowloading... %s" %animation[i % len(animation)])
		sys.stdout.flush()
		i+=1
		time.sleep(0.5)

def download(url,directory):
	global x
	temp_fold=os.getcwd()+"/temp/"
	temp_fold=os.path.normpath(temp_fold)
	if not os.path.exists(temp_fold):
		os.makedirs(temp_fold)
	r=requests.get(url).text
	soup=BeautifulSoup(r,'html.parser').find('div',attrs={'class':'container-chapter-reader'}).find_all('img')
	k=1
	files=[]
	x=0
	t=threading.Thread(target=progress)
	t.start()
	for i in soup:
		down_url=i.get('data-src')
		if "\\" in temp_fold:
			imgpath=temp_fold+"\\"+str(k)+".jpg"
		else:
			imgpath=temp_fold+"/"+str(k)+".jpg"
		files.append(imgpath)
		r=requests.get(down_url,allow_redirects=True)
		open(imgpath, 'wb').write(r.content)
		k=k+1
	x=1
	print("\nAlmost Done...Finishing the process")
	filename=re.search('/chapter/(.*)',url).group()[9:]
	for i in ['/','\\','*','<','>','|','?',':','"']:
		filename=filename.replace(i," ")
	if "\\" in temp_fold:
		filename="\\"+filename
	else:
		filename="/"+filename
	with open(directory+filename+".pdf", "wb") as f:
		f.write(img2pdf.convert([i for i in files if i.endswith(".jpg")]))
	shutil.rmtree(temp_fold)
	print(filename[1:]+" Downloaded Successfully")


