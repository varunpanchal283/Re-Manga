import requests
import os
from bs4 import BeautifulSoup
from PIL import Image
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

def download(url,directory,filename):
	global x
	temp_fold=os.getcwd()+"/temp/"
	temp_fold=os.path.normpath(temp_fold)
	if not os.path.exists(temp_fold):
		os.makedirs(temp_fold)
	r=requests.get(url+"/all-pages").text
	soup=BeautifulSoup(r,'html.parser').find_all('img',attrs={'class':'img-responsive'})
	k=1
	files=[]
	x=0
	t=threading.Thread(target=progress)
	t.start()
	for i in soup:
		down_url="https:"+i.get('src')
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
	for i in ['/','\\','*','<','>','|','?',':','"']:
		filename=filename.replace(i," ")
	if "\\" in temp_fold:
		filename="\\"+filename
	else:
		filename="/"+filename
	image=[]
	for i in range(len(files)):
		image.append(Image.open(files[i]))
	if len(image)!=1:
		image[0].save(directory+filename+".pdf", "PDF" ,resolution=100.0, save_all=True, append_images=image[1:])
	else:
		image[0].save(directory+filename+".pdf", "PDF" ,resolution=100.0, save_all=True, append_images=image)
	shutil.rmtree(temp_fold)
	print(filename[1:]+" Downloaded Successfully")
