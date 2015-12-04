# Create your views here.
from django.shortcuts  import render_to_response
from django.template import RequestContext
from biblioteca.apps.libros.models import *#Prestamo, Autor, Editorial, Categoria, Bibliotecario, Usuario, Ciudad, Tipo_Usuario, Libro, Biblioteca
from datetime import date
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import login, logout, authenticate
from biblioteca.apps.home.forms import *#libronuevo_form,Login_form
import django

from biblioteca.apps.libros.models import Espacio
from django.core import serializers

from django.utils import simplejson
from django.core.mail import EmailMultiAlternatives

from django.http import Http404

def detail(request, poll_id):
    try:
        poll = Poll.objects.get(pk=poll_id)
    except Poll.DoesNotExist:
        raise Http404
    return render(request, 'home/404.html', {'poll': poll})

def index_view (request):
	return render_to_response('home/index.html', context_instance = RequestContext(request))
#administador
def administrar_view (request):
	return render_to_response('libros/administrar.html', context_instance = RequestContext(request))
def reservas_view (request):
	reservas = Prestamo.objects.filter(estado_prestamo="Reservado").order_by('-id')
	ctx = {'reservas' :reservas}
	return render_to_response ('home/reservas.html', ctx, context_instance = RequestContext(request))

#Reservas de los usuarios registrados
def mis_reservas_view (request):
	reservas = Prestamo.objects.filter(usuario__user = request.user).order_by('-id')
	ctx = {'reservas' :reservas}
	return render_to_response('home/mis_reservas.html', ctx, context_instance = RequestContext(request))



def prestamos_view(request):
	tipo = Prestamo.objects.filter().order_by('-id')
	ctx = {'prestamos' :tipo}
	return render_to_response ('home/prestamos.html', ctx, context_instance = RequestContext(request))

def single_prestamo_view(request, id_editprest):
	editprest = Prestamo.objects.get(id = id_editprest)
	ctx = {'prestamo':editprest}
	return render_to_response('home/single_prestamo.html',ctx,context_instance = RequestContext(request))




#bibliotecario
def  bibliotecarios_view (request):
	if request.method=="POST":
	
		if "product_id" in request.POST:
			try:
				l = None
				id_usuario = request.POST['product_id']
				p = Usuario.objects.get(pk=id_usuario)
				u = User.objects.get (pk = p.user.id)
				try:
					l = Prestamo.objects.get(usuario__id = id_usuario, usuario__user__id = u.id)
				except:
					l = None
				if l == None:
					u.delete()
					#p.delete()
					mensaje={"status":"True","product_id":p.id}
				return HttpResponse(simplejson.dumps(mensaje),mimetype='application/json')
			except:
				mensaje={"status":"False"}
				return HttpResponse(simplejson.dumps(mensaje),mimetype='application/json')
	biblio = Usuario.objects.filter(tipo_usuario__nombre = 'bibliotecario')
	ctx = {'bibliotecarios': biblio}
	return render_to_response ('home/bibliotecarios.html', ctx, context_instance = RequestContext(request))

def single_bibliotecarios_view(request, id_biblio):
	usua = Usuario.objects.get(id = id_biblio)
	ctx = {'usuario':usua}
	return render_to_response('home/single_usuario.html',ctx,context_instance = RequestContext(request))

#usuario
def usuarios_view(request):
	
	if request.method=="POST":
	
		if "product_id" in request.POST:
			try:
				l = None
				id_usuario = request.POST['product_id']
				p = Usuario.objects.get(pk=id_usuario)
				u = User.objects.get (pk = p.user.id)
				try:
					l = Prestamo.objects.get(usuario__id = id_usuario, usuario__user__id = u.id)
				except:
					l = None
				if l == None:
					u.delete()
					#p.delete()
					mensaje={"status":"True","product_id":p.id}
				return HttpResponse(simplejson.dumps(mensaje),mimetype='application/json')
			except:
				mensaje={"status":"False"}
				return HttpResponse(simplejson.dumps(mensaje),mimetype='application/json')
	p = Usuario.objects.all()
	ctx = {'usuarios':p}
	return render_to_response ('home/usuarios.html', ctx, context_instance = RequestContext(request))

def single_usuario_view(request, id_usua):
	usua = Usuario.objects.get(id = id_usua)
	ctx = {'usuario':usua}
	return render_to_response('home/single_usuario.html',ctx,context_instance = RequestContext(request))

#tipo_usuario
def tipos_usuarios_view(request):


	if request.method=="POST":
	
		if "product_id" in request.POST:
			try:
				l = None
				id_product = request.POST['product_id']
				p = Tipo_Usuario.objects.get(pk=id_product)
				try:
					l = Usuario.objects.get(tipo_usuario__id = id_product)
				except:
					l = None
				if l == None:
					p.delete()
					#p.delete()
					mensaje={"status":"True","product_id":id_product}
				return HttpResponse(simplejson.dumps(mensaje),mimetype='application/json')
			except:
				mensaje={"status":"False"}
				return HttpResponse(simplejson.dumps(mensaje),mimetype='application/json')


	tipo = Tipo_Usuario.objects.all()
	ctx = {'tipos_usuarios' :tipo}
	return render_to_response ('home/tipo_usuario.html', ctx, context_instance = RequestContext(request))

def single_tipo_usuario_view(request, id_tipo):
	tipo = Tipo_Usuario.objects.get(id = id_tipo)
	ctx = {'tipos_usuarios' :tipo}
	return render_to_response ('home/single_tipo.html', ctx, context_instance = RequestContext(request))






def espacios_view (request):
	if request.method=="POST":
	
		if "product_id" in request.POST:
			try:
				l = None
				id_product = request.POST['product_id']
				p= Espacio.objects.get(pk=id_product)
				try:
					l = Prestamo.objects.get(espacio__id = id_product)
				except:
					l = None
				if l == None:
					p.delete()
					#p.delete()
					mensaje={"status":"True","product_id":id_product}
				return HttpResponse(simplejson.dumps(mensaje),mimetype='application/json')
			except:
				mensaje={"status":"False"}
				return HttpResponse(simplejson.dumps(mensaje),mimetype='application/json')
	lista_l = Espacio.objects.all()
	ctx = {'espacios' :lista_l}
	return render_to_response('home/espacios.html',ctx, context_instance = RequestContext(request))

	

def single_espacio_view (request, id_prod): 
	prod = Espacio.objects.get(id = id_prod)
	#cat = prod.categoria.all()
	ctx = {'espacio':prod}# 'categoria': cat}
	return render_to_response('home/single_espacio.html',ctx, context_instance = RequestContext(request))

def espacionuevo_view(request):
	info = "inicializando"
	fecha_inicio = ""
	nuevos = []
	h = date.today()
	mensaje = ""

	if request.method == "POST":
		formulario = espacionuevo_form(request.POST)
		if formulario.is_valid():
			
			info = True 
			fecha_inicio = formulario.cleaned_data['fecha_inicio']
			
			if fecha_inicio < h:
				nuevos = espacio.objects.filter(fecha_publicacion__range =(fecha_inicio, h))#se hace un rango de los ultimos libros comprados
			else:
				mensaje = "no hay espacios"

			formulario = espacionuevo_form()
		ctx = {'form':formulario, 'informacion':info, 'nuevos':nuevos, 'mensaje':mensaje}
		return render_to_response ('home/espacionuevo.html', ctx,context_instance =RequestContext(request))

	else:
		formulario = espacionuevo_form()
	ctx = {'form':formulario, 'informacion':info, 'nuevos':nuevos, 'mensaje':mensaje}
	return render_to_response ('home/espacionuevo.html', ctx,context_instance =RequestContext(request))

def login_view(request):
	mensaje = ""
	if request.user.is_authenticated():
		return HttpResponseRedirect('/')
	else:
		if request.method == "POST":
			formulario = Login_form(request.POST)
			if formulario.is_valid():
				usu = formulario.cleaned_data['usuario']
				pas = formulario.cleaned_data['clave']
				usuario = authenticate(username = usu, password = pas)
				if usuario is not None and usuario.is_active:
					login(request, usuario)
					return HttpResponseRedirect('/')
				else:
					mensaje = "usuario y/o clave incorrecta"
		formulario = Login_form()
		ctx = {'form':formulario, 'mensaje':mensaje}
		return render_to_response ('home/login.html', ctx, context_instance =RequestContext(request))

def logout_view(request):
	logout(request)
	return HttpResponseRedirect('/')

def ws_espacio_view(request):
		data = serializers.serialize("json",Espacio.objects.filter())
		return HttpResponse(data, mimetype = 'application/json')

