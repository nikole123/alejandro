#-*-coding: utf-8-*-
from django.shortcuts import render_to_response, render
from django.template import RequestContext
from biblioteca.apps.libros.forms import *#add_prestamo_form, add_autor_form, delete_prestamo_form, edit_prestamo_form, edit_autor_form, add_editorial_form, add_categoria_form, add_bibliotecario_form, edit_bibliotecario_form, add_usuario_form, edit_usuario_form, add_ciudad_form, edit_ciudad_form, add_tipo_usuario_form, agregar_libro_form, agregar_biblioteca_form
from biblioteca.apps.libros.models import *#Prestamo, Autor, Editorial, Categoria, Bibliotecario, Usuario, Ciudad, Tipo_Usuario, Libro, Biblioteca
from django.http import HttpResponseRedirect, HttpResponse

from django.contrib.auth.models import User
from datetime import date
import django

from django.utils import simplejson



def administrar_view (request):
	return render_to_response('libros/administrar.html', context_instance = RequestContext(request))
def consultas_view (request):
	return render_to_response('libros/consultas.html', context_instance = RequestContext(request))

# PASO 1 reservar siver para  Bibliotecario y para usuarios registrados
def reservar_view(request,id_espacio): #crear una reserva en estado RESERVADO
	if request.user.is_authenticated:# and request.user.is_staff:
		info = "" 
		#if request.user_is_authenticated() and request.user_is_staff():#modificado el 10 de abril
		if request.method == "POST": #si es POST
			formulario = add_prestamo_form(request.POST)
			if formulario.is_valid():
				add = formulario.save(commit =False)
				x = Espacio.objects.get(id=id_espacio)# modificacion 20 marzo 2015
				add.espacio = x
				if date.today() <= add.fecha_devolucion:
					try: #guarda datos del bibliotecario al e
						y = Usuario.objects.get(tipo_usuario__nombre = "bibliotecario", user_id = request.user.id)
						#add.tipo_usuario = "bibliotecario"
						add.usuario = y
						add.bibliotecario = y.nombre
						add.estado_prestamo = "Efectuado"

						print request.user 
					except:
						print "Debe estar logueado"
					#estado_prestamo reservado, cancelado, efectuado
					try:
						if request.user.is_authenticated:# and request.user_is_staff:
							add.usuario = Usuario.objects.get(user__id = request.user.id)
							usu = add.usuario
							if usu.tipo_usuario.nombre != "bibliotecario":
								usu.tiene_prestamo = True
								print "wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww"
								usu.save()
					except:
						info = "No se pudo guardar" # +++
					if x.disponibilidad == True:
						add.estado_prestamo = "Reservado"
						x.disponibilidad = False
					else:
						mensaje="El espacio no esta disponible"
					x.save()

					#validacion de la fecha de fecha_devolucion no mayor a 3 dias
					if   add.fecha_devolucion.day <= date.today().day + 3 :

						add.save() # guarda la informacion
						info = "Guardado satisfactoriamente"
						if request.user.usuario.tipo_usuario != "bibliotecario":
							return HttpResponseRedirect('/mis_reservas/')
						else:
							return HttpResponseRedirect ('/prestamos/')
					else:
						info="La devolución no debe ser mayor a 3 días"
				else:
					info="Error! La fecha de devolución ingresada no puede ser menor a la fecha actual "
		else:
			formulario = add_prestamo_form()
		ctx = {'form':formulario, 'informacion': info}
		return render_to_response('libros/add_prestamo.html', ctx, context_instance = RequestContext(request))
	else:
		return HttpResponseRedirect ('/')
#PASO 2 aprobar el prestamo del libro LO REALIZA EL BIBLIOTECARIO
def aprobar_prestamo_view (request, id_prestar):
	if request.user.is_authenticated and request.user.is_staff:
		reservado = Prestamo.objects.get(id = id_prestar) 
		reservado.estado_prestamo = "Efectuado"

		reservado.save()
		return HttpResponseRedirect('/prestamos/')
	else:
		return HttpResponseRedirect ('/')
#PASO 3 puede servir par a los 2 usuarios que reservan BLIBLIOTECARIO y USUARIO REGISTRADO
def cancelar_prestamo_view (request, id_prestar):
	if request.user.is_authenticated:
		reservado = Prestamo.objects.get(id = id_prestar) 
		reservado.estado_prestamo = "Cancelado"
		

		#reservado.libro.disponibilidad = True
		li =  reservado.espacio
		li.disponibilidad = True
		li.save()

		usu = reservado.usuario
		usu.tiene_prestamo = False
		print "wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww"
		usu.save()

		#dev = cancelar prestamo
		reservado.save()
		if request.user.is_authenticated and request.user.is_staff:
			return HttpResponseRedirect('/prestamos/')
	else:
		return HttpResponseRedirect ('/')
#PASO 4 VISTA PARA RETORNAR  LIBRO EN EL CUAL CAMBIE EL ESTADO DEL LIBRO A DISPONIBLE
def retornar_libro_view(request, id_prestar):
	if request.user.is_authenticated and request.user.is_staff:
		usu = ""
		pres = Prestamo.objects.get(pk = id_prestar)
		pres.fecha_devolucion = date.today()
		pres.estado_prestamo = 'Devuelto'
		li = pres.espacio#.disponibilidad = True
		li.disponibilidad = True
		li.save()

		usu = pres.usuario
		usu.tiene_prestamo = False
		print "wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww"
		usu.save()


		pres.save()
		return HttpResponseRedirect('/prestamos/')
	else:
		return HttpResponseRedirect ('/')
#PRESTA EL LIBRO EL BIBLIOTECARIO
def prestar_view(request, id_prestar):  #modificado el 17 de abril Funcion prestar
	if request.user.is_authenticated and request.user.is_staff:
		info = ""
		usu = ""
		pres = Prestamo.objects.get(pk = id_prestar)
		if usu:
			try:
				usu = Usuario.objects.get(tipo_usuario__nombre = "bibliotecario", user_id = request.user.id)
				pres.estado_prestamo = "Efectuado"
				pres.bibliotecario = usu.nombre
				pres.save()
				info = "Guardo Satisfactoriamente"
			except:
				print "No se pudo efectuar el préstamo"
				return HttpResponseRedirect ('/prestamo/%s'%(pres.id))
	else:
		return HttpResponseRedirect ('/')
#	ctx = {'form':formulario, 'informacion':info}
#	return render_to_response('libros/edit_prestamo.html',ctx , context_instance = RequestContext(request))

''' Fin bloque Reser'''

def edit_prestamo_view(request, id_editprest):
	if request.user.is_authenticated and request.user.is_staff:
		info = ""
		editprest = Prestamo.objects.get(pk = id_editprest)
		if request.method == "POST":
			formulario = add_prestamo_form(request.POST, instance=editprest)
			if formulario.is_valid():
				edit_prestamo = formulario.save(commit = False)
				
				edit_prestamo.save()
				info = "Guardo satisfactoriamente"
				return HttpResponseRedirect ('/prestamos/')

		else:
			formulario = add_prestamo_form(instance = editprest)

		ctx = {'form':formulario, 'informacion':info}
		return render_to_response('libros/edit_prestamo.html',ctx , context_instance = RequestContext(request))
	else:
		return HttpResponseRedirect ('/')
def eliminar_prestamo_view(request, id_prest):
	if request.user.is_authenticated and request.user.is_staff:

		info = "El préstamo se elimino safisfactoriamente"
		prest = Prestamo.objects.get(pk = id_prest)
		try:
			prest.delete()
			return HttpResponseRedirect ('/prestamos/')

		except:
			info = "La préstamo no existe"
			return HttpResponseRedirect ('/prestamos/')
	else:
		return HttpResponseRedirect ('/')


def add_bibliotecario_view(request):
	
	if request.user.is_authenticated and request.user.is_staff:
		info = "inicializando"
		if request.method == "POST":
			formulario = add_bibliotecario_form(request.POST)
			if formulario.is_valid():
				add = formulario.save(commit = False)

				add.save() # guarda la informacion
			# guarda las relaciones ManyToMany
				info = "Guardado Satisfactoriamente"
				
				return HttpResponseRedirect ('/bibliotecarios/')
		else:
			formulario = add_bibliotecario_form()
		ctx = {'form':formulario, 'informacion':info}
		return render_to_response('libros/add_bibliotecario.html', ctx,context_instance = RequestContext(request))
	else:
		return HttpResponseRedirect ('/')
def edit_bibliotecario_view(request, id_biblio):
	if request.user.is_authenticated and request.user.is_staff:

		info = ""
		biblio = Bibliotecario.objects.get(pk = id_biblio)
		if request.method == "POST":
			formulario = add_bibliotecario_form(request.POST, instance= biblio )
			if formulario.is_valid():
				edit_biblio = formulario.save(commit = False)
		
				edit_biblio.save()
				info = "Guardado Satisfactoriamente"
				return HttpResponseRedirect('/bibliotecarios/')
		else:
			formulario = add_bibliotecario_form(instance = biblio)
		ctx = {'form':formulario, 'informacion':info}
		return render_to_response('libros/edit_bibliotecario.html', ctx,context_instance = RequestContext(request))
	else:
		return HttpResponseRedirect ('/')
def del_bibliotecario_view(request, id_biblio):
	if request.user.is_authenticated and request.user.is_staff:

		info = "inicializando"
		biblio = Bibliotecario.objects.get(pk = id_biblio)
		try:
			biblio.delete()
			return HttpResponseRedirect('/bibliotecarios')
		except:
			info = "Bibliotecario no se puede eliminar"
			return HttpResponseRedirect('/bibliotecarios')
	else:
		return HttpResponseRedirect ('/')

#usuario
def add_usuario_view(request):
	if request.user.is_authenticated and request.user.is_staff:

		info = "inicializando"
		if request.method == "POST": #si es POST
			formulario = add_usuario_form(request.POST)
			if formulario.is_valid():
				add = formulario.save(commit =False)
				add.save() # guarda la informacion
				info = "Guardado Satisfactoriamente"
				return HttpResponseRedirect ('/usuarios/')
		else:
			formulario = add_usuario_form()
		ctx = {'form':formulario, 'informacion': info}
		return render_to_response('libros/add_usuario.html', ctx,context_instance = RequestContext(request))
	else:
		return HttpResponseRedirect ('/')
def edit_usuario_view(request, id_usua):
	if request.user.is_authenticated :

		now = date.today()
		m=True
		mensaje = ""
		fecha_nac=""
		mensaje = ""
		usua = Usuario.objects.get(pk = id_usua)
	
		if request.method == "POST":
			if request.user.usuario.tipo_usuario.nombre == "bibliotecario":
				if usua.tipo_usuario.nombre == "bibliotecario":
					x = date.today().year - 18
					mensaje =" Lo sentimos pero no puedes registrarte porque debe ser mayor de 18 años"
					formulario = add_bibliotecario_form(request.POST, request.FILES, instance=usua)
					#tipo_usuario 	= formulario.cleaned_data['tipo_usuario']		
				else:
					x = date.today().year - 7
					mensaje =" Lo sentimos pero no puedes editar tu información porque debe ser mayor de 7 años"		
					formulario = add_usuario_form(request.POST, request.FILES, instance=usua)	
			else:
				x = date.today().year - 7
				mensaje =" Lo sentimos pero no puedes registrarte porque debe ser mayor de 7 años"		
				formulario = add_usuario_form(request.POST, request.FILES, instance=usua)
			formulario_user = edit_user_form(request.POST, instance = usua.user)
			if formulario.is_valid() and formulario_user.is_valid():
				y = formulario.cleaned_data['fecha_nac']
				if  y.year  <=  x :
					edit_usua = formulario.save(commit = False)
					edit_usua.save()
					usua.user.set_password(formulario_user.cleaned_data['clave'])
					formulario_user.save()
					mensaje = "Guardado Satisfactoriamente"
					return HttpResponseRedirect('/')
			else:
				mensaje = mensaje	
		else:
			if request.user.usuario.tipo_usuario.nombre == "bibliotecario":
				formulario = add_bibliotecario_form(instance = usua)	
			else:
				formulario = add_usuario_form(instance = usua)
			formulario_user = edit_user_form(instance = usua.user)
		ctx = {'form':formulario, 'informacion':mensaje, 'form_user': formulario_user,'now':now, 'mensaje':mensaje}
		return render_to_response('libros/edit_usuario.html', ctx,context_instance = RequestContext(request))
	else:
		return HttpResponseRedirect ('/')


def del_usuario_view(request,id_usua):	
	info = "Se inicio proceso de eliminacion del usuario"
	usua = Usuario.objects.get(pk = id_usua)
	
	try:
		usua.delete()
		return HttpResponseRedirect ('/usuarios')

	except:
		info= "El Usuario que desea eliminar no existe"
		#return render_to_response('home/usuario.html')
		return HttpResponseRedirect ('/usuarios')

#tipo_usuario
def add_tipo_usuario_view(request):
	now = date.today()
	m=True
	if request.user.is_authenticated and request.user.is_staff:

		info = ""
		if request.method == "POST": #si es POST
			formulario = add_tipo_usuario_form(request.POST)
			if formulario.is_valid():
				add = formulario.save(commit =False)
				add.save() # guarda la informacion
				info = "Guardado satisfactoriamente"
				ctx = {'form':formulario, 'now':now, 'm':m}
				return render_to_response('libros/add_tipo.html', ctx,context_instance = RequestContext(request))
		else:
			formulario = add_tipo_usuario_form()
		ctx = {'form':formulario, 'informacion': info, 'now':now}
		return render_to_response('libros/add_tipo.html', ctx,context_instance = RequestContext(request))
	
	else:
		return HttpResponseRedirect ('/')
def edit_tipo_usuario_view(request, id_tipo):
	if request.user.is_authenticated and request.user.is_staff:

		info = ""
		tipo = Tipo_Usuario.objects.get(pk = id_tipo)
		if request.method == "POST":
			formulario = add_tipo_usuario_form(request.POST, request.FILES, instance=tipo)
			if formulario.is_valid():
				edit_tipo = formulario.save(commit = False)
				
				edit_tipo.save()
				info = "Guardo Satisfactoriamente"
				return HttpResponseRedirect ('/tipos_usuarios/')

		else:
			formulario = add_tipo_usuario_form(instance = tipo)

		ctx = {'form':formulario, 'informacion':info}
		return render_to_response('libros/edit_tipo.html',ctx , context_instance = RequestContext(request))
	else:
		return HttpResponseRedirect ('/')	
def eliminar_tipo_usuario_view(request, id_tipo):
	if request.user.is_authenticated and request.user.is_staff:

		info = "El tipo de usuario se elimino satisfactoriamente"
		try:
			tipo = Tipo_Usuario.objects.get(pk = id_tipo)
			tipo.delete()
			return HttpResponseRedirect('/tipos_usuarios')
		except:
			info = "El tipo de usuario que desea eliminar no existe"
			return HttpResponseRedirect ('/tipos_usuarios')   
	else:
		return HttpResponseRedirect ('/')



def agregar_espacio_view (request):
	now = date.today()
	m=True
	if request.user.is_authenticated and request.user.is_staff:

		info = ""
		mensaje = ""

		if request.method == "POST":
			formulario = agregar_espacio_form(request.POST, request.FILES)
			if formulario.is_valid():
				add = formulario.save(commit = False)
				#add.fecha_adquisicion
				#add.fecha_publicacion
				if add.fecha_adquisicion >=add.fecha_publicacion:


					add.save()
					ctx = {'form':formulario, 'now':now, 'm':m}
					info = "Guardado satisfactoriamente"
					return render_to_response('libros/agregar_espacio.html', ctx,context_instance = RequestContext(request))
				else:
					mensaje="Error ! La fecha de adquisición ingresada no puede ser menor a la de publicación "
		else:
			formulario = agregar_libro_form()
		ctx = {'form':formulario, 'informacion':info, 'mensaje': mensaje, 'now':now}
		return render_to_response('libros/agregar_espacio.html', ctx,context_instance = RequestContext(request))
	else:
		return HttpResponseRedirect ('/')
#Nuevo
def editar_espacio_view (request, id_prod):
	if request.user.is_authenticated and request.user.is_staff:

		info = ""
		prod = Espacio.objects.get(pk = id_prod)
		if request.method == "POST":
			formulario = agregar_espacio_form(request.POST,request.FILES, instance= prod) #FILES para agregar imagenes
			if formulario.is_valid():
				edit_prod = formulario.save(commit = False)
				formulario.save_m2m()
				edit_prod.save()
				info = "Guardado satisfactoriamente"
				return HttpResponseRedirect ('/espacio/%s'%(prod.id))
				
		else:
			formulario = agregar_espacio_form(instance = prod)

		ctx = {'form':formulario, 'informacion':info}
		return render_to_response('libros/editar_espacio.html', ctx,context_instance = RequestContext(request))
	else:
		return HttpResponseRedirect ('/')
#ELIMINAR LIBRO 
def del_view (request, id_prod): #obteniendo el objeto a eliminar 
	if request.user.is_authenticated and request.user.is_staff:
	
		info = "Se inicio el proceso de eliminación"
		l = None # nul o vacio donde se puede almacenar un objeto
		#opc2 = []
		prod = Espacio.objects.get(pk = id_prod)

		try: 
			l=prestamo.objects.get(espacio__id =prod.id )
			#opc2 = prestamo.objects.filter( libro__id=prod.id)
		except: 
			pass

		if l== None: 

			try:
				prod.delete()
				return HttpResponseRedirect ('/espacios')#cuando no se trabaja con paginator se agrega sin numero 
			except: 
				info = "EL espacio que desea eliminar no existe"
				return HttpResponseRedirect ('/espacios')
		else: 
				info = "El espacio no se puede eliminar ya que existe algun préstamo asociado"		
				return HttpResponseRedirect ('/espacios')
	else:
		return HttpResponseRedirect ('/')


def consultar_usuario_id_view(request):
	if request.user.is_authenticated and request.user.is_staff:
		mensaje = ""
		usua =""
		if request.user.is_authenticated():
			if request.method == "POST":
				formulario	 = consultar_usuario_id_form(request.POST) #creamos un objeto de Loguin form
				if formulario.is_valid(): #si la informacion enviada es correcta
					tipo_id=formulario.cleaned_data['tipo_id']
					ide= formulario.cleaned_data['identificacion'] #guarda informacion ingresada del formulario
					try:
						usua=Usuario.objects.get(tipo_id=tipo_id,identificacion=ide)
						mensaje = "Se encontro el usuario con el numero de identificación " + ide + " sus Datos son:"

						#return HttpResponseRedirect('/usuario/%s'%usua.id)		
					except:
						mensaje = "Usuario no encontrado" #verificampos si el usuario ya esta autenticado o logueado}
				else:
					mensaje = "El campo no debe estar vacio, por favor ingrese un valor"
							
		 #si esta logueando lo redirigimos a la pagina principal
		else: #si no esta authenticado
			return HttpResponseRedirect('/')
		formulario = consultar_usuario_id_form() #creamos un formulario nuevo en limpio
		ctx = {'form':formulario, 'mensaje':mensaje, 'usuario':usua} # variable de contexto para pasar info a login.html
		return render_to_response('home/consultar.html', ctx,context_instance = RequestContext(request))
	else:
		return HttpResponseRedirect ('/')


#register view

def register_view(request):
		now = date.today()
		m=True
		mensaje = ""
		fecha_nac=""
		if request.method == "POST":
			
			form_a = RegisterForm(request.POST)
			form_b = add_usuario_form(request.POST,request.FILES, prefix = "b")
			if form_b.is_valid() and form_a.is_valid():
				usuario 		= form_a.cleaned_data['username']
				email 			= form_a.cleaned_data['email']
				password_one	= form_a.cleaned_data['password_one']
				password_two 	= form_a.cleaned_data['password_two']
				tipo_usuario 	= form_b.cleaned_data['tipo_usuario']

				if  form_b.cleaned_data['fecha_nac'] < now:
				
					x = date.today()
					y = form_b.cleaned_data['fecha_nac']
					if  y.year  <=  x.year - 7 : 
						try:
							u = User.objects.create_user(username = usuario,email = email, password = password_one)
							u.save() #guarda el objeto
							b = form_b.save(commit=False)
							b.tipo_usuario = tipo_usuario
							b.user= u 
							b.save()
						except:
							pass
						ctx = {'form_a':form_a, 'form_b':form_b, 'now':now, 'm':m}
						#return HttpResponseRedirect ('/registro')
						return render_to_response('home/register.html/', ctx,context_instance = RequestContext(request))
					else:
						mensaje =" Lo sentimos, pero no puedes registrarte porque debes ser mayor de 7 años"
				else:
					mensaje = "Error! La fecha de nacimiento debe ser menor  a la fecha actual"	
			else:
				mensaje = "falló llene todos los campos"

		else:
			form_a = RegisterForm()
			form_b = add_usuario_form(prefix = "b")
		ctx = {'form_a':form_a, 'form_b':form_b, 'now':now, 'mensaje':mensaje}	
		return render_to_response ('home/register.html',ctx, context_instance= RequestContext(request))	
		


#REGISTRAR BIBLIOTECARIO ---
def register_bibliotecario_view(request):
	
	if request.user.is_authenticated and request.user.is_staff:
		now = date.today()
		m=True	
		info = ""
		fecha_nac=""
		if (request.user.is_authenticated() and request.user.is_staff and request.user.is_superuser):
			if request.method == "POST":
				form_a = RegisterForm(request.POST)
				form_b = add_bibliotecario_form(request.POST, request.FILES,  prefix = "b")
				if form_b.is_valid() and form_a.is_valid():
					usuario 		= form_a.cleaned_data['username']
					email 			= form_a.cleaned_data['email']
					password_one	= form_a.cleaned_data['password_one']
					password_two 	= form_a.cleaned_data['password_two']

					if  form_b.cleaned_data['fecha_nac'] < now:
						#evalua si la fecha ingresada es mayor de 18 años 
						x = date.today()
						y = form_b.cleaned_data['fecha_nac']
						if  y.year  <=  x.year - 18: 
							try:
								tipo = Tipo_Usuario.objects.get(nombre='bibliotecario')
								if tipo:
									u = User.objects.create_user(username = usuario,email = email, password = password_one)
									b = form_b.save(commit=False)
									b.tipo_usuario = tipo
									u.is_staff = True
									u.is_superuser = True
									u.save() #guarda el objeto USER
									b.user = u 
									b.save() #guarda el objeto USUARIO
									ctx = {'form_a':form_a, 'form_b':form_b, 'now':now, 'm':m}
									return render_to_response('home/register_b.html/', ctx,context_instance = RequestContext(request))
							except:
								info = "No se puede crear un bibliotecario porque no existe un tipo de usuario 'bibliotecario'"
								#ctx = {'form_a':form_a, 'form_b':form_b, 'now':now, 'm':m}
								#return render_to_response('home/register_b.html/', ctx,context_instance = RequestContext(request))
							#return render_to_response('home/confirmacion.html',context_instance = RequestContext(request))
						else:
							info ="Lo sentimos pero no puedes registrar un bibliotecario menor de 18 años"	
					else:
						info = "Error! La Fecha de nacimiento debe ser menor  a la fecha actual"	
				else:
					info = "fallo llene todos los campos"	
			else:
				form_a = RegisterForm()
				form_b = add_bibliotecario_form(prefix = "b")
			ctx = {'form_a':form_a, 'form_b':form_b, 'now':now, 'info':info}	
			return render_to_response ('home/register_b.html',ctx, context_instance= RequestContext(request))	

		else: #por sino es super administrador
			return HttpResponseRedirect('/bibliotecarios/')
	else:
		return HttpResponseRedirect ('/')

#


def info_view (request):
	return render_to_response('home/info.html', context_instance = RequestContext(request))