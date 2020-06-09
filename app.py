import cherrypy
import os
from database import *
from functions import *
from PIL import Image

config = {
  "/":     { "tools.staticdir.root": os.path.dirname(os.path.abspath(__file__)) },

  "/croppedImages": { "tools.staticdir.on": True,
				   "tools.staticdir.dir": "Webpage/croppedImages"},

  "/js":		 { "tools.staticdir.on": True,
				   "tools.staticdir.dir": "Webpage/assets/js" },
				   
  "/css":		 { "tools.staticdir.on": True,
				   "tools.staticdir.dir": "Webpage/assets/css" }, 
				  
  "/fonts":		 { "tools.staticdir.on": True,
						   "tools.staticdir.dir": "Webpage/assets/fonts" },

  "/bootstrap": { "tools.staticdir.on": True,
						   "tools.staticdir.dir": "Webpage/assets/bootstrap" },

  "/img":		 { "tools.staticdir.on": True,
						   "tools.staticdir.dir": "Webpage/assets/img" },
						   
  "Webpage":		 { "tools.staticdir.on": True,
						   "tools.staticdir.dir": "Webpage/html" },
}

class Root(object):
	def __init__(self):
		self.insert = Insert()
		self.search = Search()
		self.all = All()
		self.about = About()
		
	@cherrypy.expose
	def index(self):
		cherrypy.response.headers["Content-Type"] = "text/html"
		f = open("Webpage/Home.html", "r")
		data = f.read()
		return data
		
		
class Insert(object):
	@cherrypy.expose
	def index(self):
		cherrypy.response.headers["Content-Type"] = "text/html"
		f = open("Webpage/Insert.html", "r")
		data = f.read()
		return data
	
	@cherrypy.expose
	def put(self,post_file):
		whole_data = bytearray() # Neues Bytearray
		while True:
			data = post_file.file.read(8192)
			whole_data += data # Save data chunks in ByteArray whole_data
			if not data:
				break
			written_file = open("images/"+post_file.filename, "wb") # open file in write bytes mode
			written_file.write(whole_data) # write file	
			
		Create_Table()


		img_crop("images/"+str(post_file.filename))
			
				
class Search(object):
	@cherrypy.expose
	def index(self):
		cherrypy.response.headers["Content-Type"] = "text/html"
		f = open("Webpage/Search.html", "r")
		data = f.read()
		return data
		
class All(object):
	@cherrypy.expose
	def index(self):
		cherrypy.response.headers["Content-Type"] = "text/html"
		f = open("Webpage/All.html", "r")
		data = f.read()
		j = open("Webpage/jsonFiles/allData.json", "w")
		info = {}
		num = os.listdir("croppedImages")
		for directory in num:
			info[directory] = []
			cont = os.listdir("croppedImages/"+directory)
			for filename in cont:
				a = search_smh_by_smh("Confidence", "Name", filename)
				b = search_smh_by_smh("opath", "Name", filename)
				c = search_smh_by_smh("path", "Name", filename)
				d = search_smh_by_smh("Class", "Name", filename)
				e = search_smh_by_smh("RGB", "Name", filename)
				a = str(a[0]).split(",")
				b = str(b[0]).split(",")
				c = str(c[0]).split(",")
				d = str(d[0]).split(",")
				e = str(e[0]).split(",")
				a = a[0].split("(")
				b = b[0].split("(")
				c = c[0].split("(")
				d = d[0].split("(")
				e = e[0].split("(")
				info[directory].append({'class': d[1], 'original': b[1], 'image': c[1], 'name': filename, 'color': e[1], 'confidence': a[1]})
		json.dump(info, j, indent=4)
		return data
	
	@cherrypy.tools.json_out()
	@cherrypy.tools.json_in()
	@cherrypy.expose
	def classname(self , type=None):
		if(type == "names"):
			j = open("Webpage/jsonFiles/class.json", "w")
			num = os.listdir("croppedImages")
			info = {}
			info['classId'] = []
			for filename in num:
				info['classId'].append({'class': filename})
			json.dump(info, j, indent=4)
			return json.dumps(info, indent=4, sort_keys=True)
	
	@cherrypy.tools.json_out()
	@cherrypy.tools.json_in()
	@cherrypy.expose
	def allcrops(self, type=None):
		if(type == "detected"):
			j = open("Webpage/jsonFiles/allImgs.json", "w") 
			f = open("Webpage/jsonFiles/allData.json", "r") 
			num = os.listdir("croppedImages")
			datastore = json.load(f)
			info = {}
			for directory in num:
				info[directory] = []
				for obj in datastore[directory]:
					a = str(obj['original']).split("'")
					b = str(obj['image']).split("'")
					c = str(obj['confidence']).split("'")
					info[directory].append({'image': b[1], 'original': a[1], 'confidence': c[0]})
			json.dump(info, j, indent=4)
			return json.dumps(info, indent=4, sort_keys=True)
		
	@cherrypy.tools.json_out()
	@cherrypy.tools.json_in()
	@cherrypy.expose
	def imgsclass(self, name, type=None):
		if(type == "detected"):
			f = open("Webpage/jsonFiles/imgClass.json", "w")
			j = open("Webpage/jsonFiles/allData.json", "r")
			datastore = json.load(j)
			info = {}
			info[name] = []
			num = os.listdir("croppedImages")
			for obj in datastore[name]:
				a = str(obj['original']).split("'")
				b = str(obj['image']).split("'")
				c = str(obj['confidence']).split("'")
				d = str(obj['name']).split("'")
				e = str(obj['color']).split("'")
				info[name].append({'image': b[1], 'original': a[1], 'name': d[0], 'color': e[1], 'confidence': c[0]})
			json.dump(info, f, indent=4)
			return json.dumps(info, indent=4, sort_keys=True)
		
	@cherrypy.tools.json_out()
	@cherrypy.tools.json_in()
	@cherrypy.expose
	def colorclass(self, name, color, type=None):
		if(type == "detected"):
			j = open("Webpage/jsonFiles/allData.json", "r")
			f = open("Webpage/jsonFiles/colorClass.json", "w")
			info = {}
			info[name] = []
			datastore = json.load(j)
			num = os.listdir("croppedImages")
			i=0
			for directory in num:
				if(directory == name):
					for obj in datastore[directory]:
						a = str(obj['original']).split("'")
						b = str(obj['image']).split("'")
						c = str(obj['confidence']).split("'")
						d = str(obj['name']).split("'")
						e = str(obj['color']).split("'")
						if(e[1] == color):
							info[name].append({'image': b[1], 'original': a[1], 'name': d[0], 'color': e[1], 'confidence': c[0]})
			json.dump(info, f, indent=4)
			return json.dumps(info, indent=4, sort_keys=True)
		
class About(object):
	@cherrypy.expose
	def index(self):
		cherrypy.response.headers["Content-Type"] = "text/html"
		f = open("Webpage/About.html", "r")
		data = f.read()
		return data
		
if __name__ == "__main__":
	cherrypy.engine.subscribe('start', Create_Table)
	cherrypy.config.update({'server.socket_port': 10005})				###
	cherrypy.quickstart(Root(), "/", config)							###

