 #!/usr/bin/python
 # -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User

tipo_id = (
	('cedula', 'CC'),
	('ti', 'T.I'),
	('pasaporte', 'Pasaporte'),
	('libreta militar', 'Libreta Militar'),
)


#Clase "Tipo_Usuario" Yaki ft Jennifer
class Tipo_Usuario (models.Model):
	nombre = models.CharField(max_length = 100)
	def __unicode__ (self):
		return self.nombre


genero= (
	('femenino', 'Femenino'),
	('masculino', 'Masculino'),
)


#estado prestamo 
estado_prestamo = (
	('Reservado', 'Reservado'),
('Cancelado', 'Cancelado'),
('Efectuado', 'Efectuado'), 
('Devuelto', 'Devuelto'), 
	)

estado = (
	('bueno', 'Bueno'),

('regular','Regular'),
('malo', 'Malo'),
)



class Espacio (models.Model): 
	def url (self,filename): 
		ruta = "MultimediaData/Espacio/%s/%s"%(self.nombre_espacio, str(filename))
		return ruta

	nombre_espacio		=	models.CharField(max_length = 200)
	imagen				= 	models.ImageField(upload_to = url, null = True, blank = True)
	codigo				= 	models.CharField(max_length = 200, unique = True)
	estado				= 	models.CharField(max_length = 200, choices = estado)
	disponibilidad  	= 	models.BooleanField()
	observacion			= 	models.TextField(max_length= 400, null = True, blank = True)
	fecha_publicacion	= 	models.DateField()
	fecha_adquisicion	= 	models.DateField()
	

	def __unicode__(self):
		return self.nombre_espacio


class Usuario (models.Model):

	def url (self,filename):
		ruta = "MultimediaData/Users/%s/%s"%(self.user.username, str(filename))
		return ruta

	nombre         			 = 	models.CharField(max_length = 100)
	apellido       			 = 	models.CharField(max_length = 100)
	tipo_id					 = 	models.CharField(max_length = 100, choices = tipo_id)
	identificacion     	   	 = 	models.CharField(max_length = 100, unique = True)
	fecha_nac       	     = 	models.DateField()
	genero					 = 	models.CharField(max_length = 200, choices = genero)
	tipo_usuario             =	models.ForeignKey(Tipo_Usuario)
	user 					 =	models.OneToOneField(User)
	photo 					 =	models.ImageField(upload_to = url, null = True, blank = True)
	tiene_prestamo 			 =	models.BooleanField(default = False)

	def __unicode__ (self):
		return self.nombre 

#Clase "Bibliotecario" Stefy ft Angie 
class Bibliotecario (models.Model):
	nombre 			= models.CharField(max_length = 200)
	apellidos		= models.CharField(max_length = 200)
	telefono		= models.CharField(max_length = 200)
	direcccion		= models.CharField(max_length = 200)
	correo			= models.CharField(max_length = 200)
	genero			= models.CharField(max_length = 200, choices = genero)
	#usuario 		= models.()

	def __unicode__ (self):
		return self.nombre


#clase "Prestamo" Poto, George
class Prestamo (models.Model):
	fecha_prestamo 		=  models.DateField(auto_now =True) # 
	fecha_devolucion	=  models.DateField() 
	espacio 			=  models.ForeignKey(Espacio)#
	bibliotecario   	=  models.CharField(max_length=100 , null = True, blank = True) 
	usuario 			=  models.ForeignKey(Usuario)# captura  usuario que reservo el libro 
	estado_prestamo 	=  models.CharField(max_length = 200, choices = estado_prestamo)#
	
	def __unicode__ (self):
		return self.espacio.nombre_espacio 
