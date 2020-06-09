import requests
from PIL import Image
import json
import os
from database import Insert_Item, ImgBlob

def img_recon(img):
	session = requests.Session()
	URL = "http://image-dnn-sgh-jpbarraca.ws.atnog.av.it.pt/process"
	with open(img, "rb") as f:
		file = {'img': f.read()}
		r = session.post(url=URL, files=file, data=dict(thr=0.5))
		if r.status_code == 200:
			return r.json()

list2 = []
list_rgb2 = []
list_conf2 = []

def img_crop(img):
	im = Image.open(img)
	sep = img.split(".")
	sep2 = sep[0].split("/")
	im2 = Image.new(im.mode, im.size)
	list1, list_conf2 = img_coords(img)
	j = 1
	i = 0
	list2 = []
	list_rgb2 = []
	while i <= len(list1)-1:
		box = list1[i]
		name = list1[i+1]
		filer = "croppedImages/"+str(name)
		if not os.path.exists(filer):
			os.makedirs("croppedImages/"+str(name))
			os.makedirs("Webpage/croppedImages/"+str(name))
		#im2 = Image.new(im.crop(box).mode, im.crop(box).size)
		im2 = im.crop(box)
		im3 = im.crop(box)
		nome = sep2[1]+"_"+str(j)+"."+sep[1]
		a = "croppedImages/"+str(name)+"/"+nome
		b = "Webpage/"+a
		im2.save(a)
		im3.save(b)
		list_rgb2.append(img_frequent_color(a))
		Insert_Item(ImgBlob(a), list_conf2[j-1], a, list_rgb2[j-1],str(img))
		i += 2
		j += 1
		list2.append(a)
		
	
def img_coords(img):
	a = img_recon(img)
	list1 = []
	list_conf = []
	for obj in a:
		b = (obj["box"]["x"], obj["box"]["y"], obj["box"]["x1"], obj["box"]["y1"])
		list1.append(b)
		list1.append(obj["class"])
		list_conf.append(int(100*obj["confidence"]))
	return list1, list_conf


def img_frequent_color(img):
	s=""
	im2 = Image.open(img)
	width, height = im2.size
	
	im = im2.convert('RGB')
	
	m = im.mode
	list_rgb = []
	r_t = 0
	g_t = 0
	b_t = 0
	b2_t = 0
	w_t = 0
	s=""
	list_rgb = []
	for x in range(width):
		for y in range(height):
			p = im.getpixel((x,y))
			if(p[0] < 50 and p[1] < 50 and p[2] < 50):
				b2_t += 1
			elif((p[0] > 200 and p[2] > 200) or(p[0] > 200 and p[1] > 200 ) or(p[1] > 200 and p[2] > 200) ):
				w_t += 1
			elif(p[0] > p[1] and p[0]> p[2]):
				r_t += 1
			elif(p[1] > p[0] and p[1]>p[2]):
				g_t += 1
			elif(p[2] > p[0] and p[2]>p[1]):
				b_t += 1

		'''print(r_t)	
		print(g_t)	
		print(b_t)	
		print(b2_t)	
		print(w_t)	
		print("###########################")'''
		
		if(r_t > g_t and r_t >b_t and r_t >b2_t and r_t >w_t):
			s = "red"
		elif(g_t > r_t and g_t >b_t and g_t >b2_t and g_t >w_t):
			s = "green"
		elif(b_t > g_t and b_t >r_t and b_t >b2_t and b_t >w_t):
			s = "blue"
		elif(b2_t > g_t and b2_t >r_t and b2_t >b_t and b2_t >w_t):
			s = "black"
		elif(w_t > g_t and w_t >r_t and w_t >b2_t and w_t >b_t):
			s = "white"
		else:
			s="no dominant colour"			
	return s
	
	
	
	
	
