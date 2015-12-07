from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('biblioteca.apps.libros.views',


		url(r'^administrar/$','administrar_view', name = 'vista_administrar'),
		#url(r'^add/prestamo/$','add_prestamo_view',name = 'vista_add_prestamo'),
		
		url(r'^reservar/(?P<id_libro>.*)/$','reservar_view',name = 'vista_reservar'),
		url(r'^aprobar/prestamo/(?P<id_prestar>.*)/$','aprobar_prestamo_view',name = 'vista_aprobar_prestamo'),
		url(r'^cancelar/prestamo/(?P<id_prestar>.*)/$','cancelar_prestamo_view',name = 'vista_cancelar_prestamo'),
		url(r'^retornar/espacio/(?P<id_prestar>.*)/$','retornar_espacio_view',name = 'vista_retornar_espacio'),
		
		#url(r'^prestar/(?P<id_prestar>.*)/$','prestar_view',name = 'vista_prestar'),
		
		url(r'^edit/prestamo/(?P<id_editprest>.*)/$', 'edit_prestamo_view', name = 'vista_edit_prestamo'),
		url(r'^eliminar/prestamo/(?P<id_prest>.*)/$','eliminar_prestamo_view',name= 'vista_eliminar_prestamo'),

		
		
		#usuario
		url(r'^add/usuario/$','add_usuario_view',name = 'vista_agregar_usuario'),
		url(r'^edit/usuario/(?P<id_usua>.*)/$', 'edit_usuario_view', name = 'vista_editar_usuario'),
		url(r'^del/usuario/(?P<id_usua>.*)/$', 'del_usuario_view', name = 'vista_eliminar_usuario'),
		
		url(r'^consultar_usuario_id/$','consultar_usuario_id_view', name = 'vista_consultar_usuario_id'),

		url(r'^registrar/bibliotecario/$','register_bibliotecario_view',name = 'vista_registrar_bibliotecario'),

		#tipo_usuario
		url(r'^add/tipo-usuario/$','add_tipo_usuario_view',name = 'vista_agregar_tipo'),
		url(r'^edit/tipo-usuario/(?P<id_tipo>.*)/$', 'edit_tipo_usuario_view', name = 'vista_editar_tipo'),
		url(r'^eliminar/tipo-usuario/(?P<id_tipo>.*)/$', 'eliminar_tipo_usuario_view', name = 'vista_eliminar_tipo'),

		url(r'^add/espacios/$', 'agregar_espacio_view', name = 'vista_agregar_espacios'),
		url(r'^edit/espacio/(?P<id_prod>.*)/$', 'editar_espacio_view', name = 'vista_editar_espacios'),
		url(r'^del/espacio/(?P<id_prod>.*)/$', 'del_view', name= 'vista_eliminar_cosmetico'),

		
		url(r'^registro/$','register_view', name= 'vista_registro'),


		#info sobre nosotros
		url(r'^info/$','info_view', name = 'vista_info'),

)
