import sqlite3
from PIL import Image


#Executar esta função de modo a verificar se a base de dados está criada. Caso não esteja, esta será criada com recurso à definição "IF NOT EXISTS" //
def Create_Table():														
	db = sqlite3.connect('img_database.db')								#Conecta-se à base de dados com o nome de "img_database.db"		//				
	cursor= db.cursor()													
	
	cursor.execute('''CREATE TABLE IF NOT EXISTS Images 				
					(Id INTEGER PRIMARY KEY AUTOINCREMENT, Class text NOT NULL, Name text NOT NULL, blob BLOB, Confidence real, path text NOT NULL, RGB text NOT NULL, opath text)''')
																		#Cria a Base de dados com os parâmetros acima//
	db.commit()															#Guarda as alterações//
	db.close()															#Fecha a Base de Dados//



#def List_Inserts(rgb,confidence,paths):
#	print(paths)
#	print(rgb)
#	print(confidence)
#	for row in paths:
#		blob = ImgBlob(paths[row])
#		Insert_Item(blob, confidence[row], paths[row],rgb[row])
	
def ImgBlob(image):
	with open(image, 'rb') as imgfile:                                                                        # Transformação da imagem para BLOB
		blob = imgfile.read()
	return blob


def Insert_Item(blob, confidence, path, rgb, opath):
	parts = path.split("/")
	classid=parts[1]
	name=parts[2]
	
	db = sqlite3.connect('img_database.db')								#Abertura da database e Verifica se o hashID já existe(se existir significa que a imagem é a mesma e por isso não a escreve de novo)//
	cursor= db.cursor()
	x= cursor.execute('''SELECT * FROM Images WHERE blob=?''', (blob,))
	rows = x.fetchall()
 
	for row in rows:	
		return None		
		
########################################################################	Se não existir na database:											


	
	with open(path, 'rb') as imgfile:									# Transformação da imagem para BLOB
		blob = imgfile.read()

	db = sqlite3.connect('img_database.db')								#Abertura da database
	cursor= db.cursor()
	
	
	cursor.execute("""INSERT INTO Images (Class, Name,  blob, Confidence, path, RGB, opath) VALUES(?,?,?,?,?,?,?);""", (classid, name, blob, confidence, path,rgb,opath) ) 
																		#Inserção dos parametros que são requeridos à priori pela função como argumentos

	db.commit()
	db.close()
	

def search_smh_by_smh(target, have, haveValue):
	db = sqlite3.connect("img_database.db")
	result = db.execute("SELECT "+target+" FROM Images WHERE "+have+"= \""+haveValue+"\";")
	rows = result.fetchall()
	return rows
	db.close()


def Search():
	new_dict={}
	new = []
	db = sqlite3.connect("img_database.db")
	result = db.execute("SELECT Class, Name, Confidence, path, RGB, opath FROM Images ;")
	rows = result.fetchall()
	with open('Webpage/jsonFiles/test.txt', 'w') as f:
		for item in rows:
			string = "%s\n" % str(item)
			string1 = string.replace("(", "")
			string2 = string1.replace(")","")
			words = string2.split(", ")
			new_dict['class']=words[0]
			new_dict['name']=words[1]
			new_dict['confidence']=words[2]
			new_dict['path']=words[3]
			new_dict['rgb']=words[4]
			new_dict['opath']=words[5]
			new.append(new_dict)
			f.write(str(new_dict)+"\n")
			

	db.close()
	#print(new)
	
	return new


#Insert_Item(ImgBlob("images/rua.jpg"), 100, "croppedImages/car/rua.jpg", "255.0.0")

#search_rgb("red")

