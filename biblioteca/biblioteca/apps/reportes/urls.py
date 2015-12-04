from django.conf.urls.defaults import *

urlpatterns = patterns('biblioteca.apps.reportes.views',
#	url(r'^historia/(?P<id_his>.*)/$','singleHistoria_view',name='vista_single_historia'),
	
	url(r'^reportes/$', 'reportes_view', name = 'vista_reportes'),
	
	url(r'^reportes/usuarios_por_mes/$', 'reporte_usuarios_mes_view', name = 'vista_reporte_usuarios_mes'),
	url(r'^generar_pdf_usuarios_mes/$', 'generar_pdf_usuarios_mes', name='generar_pdf_usuarios_mes'),

	
)