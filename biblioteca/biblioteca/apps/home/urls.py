from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('biblioteca.apps.home.views',
	#url(r'^$','index_view', name = 'vista_principal'),
	
	
	url(r'^espacionuevo/$','espacionuevo_view', name = 'vista_espacionuevo'),
	url(r'^login/$','login_view', name = 'vista_login'),
	url(r'^logout/$','logout_view', name = 'vista_logout'),



	#prestamos
	url(r'^prestamos/$','prestamos_view', name = 'vista_prestamos'),
	url(r'^prestamo/(?P<id_editprest>.*)/$', 'single_prestamo_view', name = 'vista_single_prestamo'),
	url(r'^reservas/$','reservas_view',name = 'vista_reservas'),
	
	url(r'^mis_reservas/$','mis_reservas_view',name = 'vista_mis_reservas'),
	
	
	#biblotecario
	url(r'^bibliotecarios/$','bibliotecarios_view', name= 'vista_bibliotecarios'),
	url(r'^bibliotecario/(?P<id_biblio>.*)/$', 'single_bibliotecarios_view', name = 'vista_single_bibliotecario'),

	#usuario
	url(r'^usuarios/$', 'usuarios_view', name = 'vista_usuarios'),
	url(r'^usuario/(?P<id_usua>.*)/$', 'single_usuario_view', name = 'vista_single_usuario'),

	

	#tipo_usuario
	url(r'^tipos_usuarios/$','tipos_usuarios_view', name = 'vista_tipos_usuarios'),
	url(r'^tipo_usuario/(?P<id_tipo>.*)/$','single_tipo_usuario_view', name = 'vista_single_tipo_usuario'),

	#libros
	url(r'^espacios/$', 'espacios_view', name = 'vista_espacios'),
	#url(r'^libros/page/(?P<pagina>.*)/$', 'libros_view', name = 'vista_libros'),
	url(r'^espacio/(?P<id_prod>.*)/$', 'single_espacio_view', name = 'vista_single_espacio'),

	
	#Webservices JSON y XML
	url(r'^ws/espacio/$','ws_espacio_view', name = 'ws_espacio_url'),


	)
