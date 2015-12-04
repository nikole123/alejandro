#-*-coding: utf-8-*-
from io import BytesIO
from django.forms import extras
from reportlab.lib import colors
from django.shortcuts import render
from reportlab.platypus import Table
from datetime import  date, timedelta
from reportlab.lib.pagesizes import letter
from django.template import RequestContext
from django.contrib.auth import authenticate
from django.views.generic import TemplateView
from django.shortcuts import render_to_response
from reportlab.lib.styles import getSampleStyleSheet
from django.http import HttpResponseRedirect, HttpResponse
from reportlab.platypus import SimpleDocTemplate, Paragraph, TableStyle
from django.core.paginator import Paginator, EmptyPage, InvalidPage

from biblioteca.apps.reportes.forms import  *
from biblioteca.apps.libros.forms import *
from biblioteca.apps.libros.models import *

import os
from reportlab.platypus import Paragraph
from reportlab.platypus import Image
from reportlab.platypus import SimpleDocTemplate
from reportlab.platypus import Spacer

from biblioteca.apps.libros.models import Espacio

from reportlab.platypus import Paragraph, Image, SimpleDocTemplate, Spacer


from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics.charts import *
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.widgets.markers  import makeMarker
from reportlab import *
#from django.http import HttpResponseRedirect
from reportlab.lib.colors import Color, blue, red, yellow

from reportlab.graphics.charts.piecharts import Pie

from reportlab.graphics.charts.legends import Legend
from reportlab.lib.enums import TA_LEFT, TA_RIGHT, TA_CENTER, TA_JUSTIFY
import datetime

from reportlab.lib.styles import getSampleStyleSheet
estilo = getSampleStyleSheet()

from reportlab.lib.units import inch

x = date.today()
y = date.today()

x1 = 0
y1 = 0
b = date.today()

def reportes_view(request):

	if request.user.is_authenticated():
		return render_to_response('home/reportes.html',context_instance = RequestContext(request)) 
	else:
		return HttpResponseRedirect('/')

def reporte_usuarios_mes_view(request):
    if request.user.is_authenticated():
        info_enviado = True
        fecha_usuarios = ""
        #hoy = date.today()
        #mes = hoy.month
        mes = 0
        anio = 0
        usuarios = []
        mensaje = ""
        error_fecha = ""
        error_vacio = ""
        

        if request.method == "POST":
            reportes = fecha_mes_form(request.POST)
            if reportes.is_valid():
                info_enviado = True
                fecha_usuarios= reportes.cleaned_data['fecha']
                if fecha_usuarios <= date.today():
                    global x
                    x = fecha_usuarios
                    mes = fecha_usuarios.month
                    anio = fecha_usuarios.year
                    usuarios = Prestamo.objects.filter(fecha_prestamo__month =mes,fecha_prestamo__year = anio)

                    global u1, u2
                    u2 = usuarios.count()
                    if (mes == 1):
                        u1= Prestamo.objects.filter(fecha_prestamo__month = mes+11, fecha_prestamo__year = anio-1).count()
                        u1m = mes+11
                    else:
                        u1= Prestamo.objects.filter(fecha_prestamo__month = mes-1, fecha_prestamo__year = anio).count()
                        u1m = mes-1



                    
                    mensaje = "Exito!"
                else:
                    error_fecha = "Error! La fecha ingresada no puede ser mayor a la fecha actual"
            else:
                error_vacio = "El campo no debe estar vacio"


        else:                                                                  
            reportes = fecha_mes_form()
        ctx = {'reporte_usuarios':reportes,'mensaje':mensaje,'error_vacio':error_vacio,'error_fecha':error_fecha, 'usuarios':usuarios, 'info_enviado':info_enviado, 'fecha_usuarios':fecha_usuarios }
        return render_to_response('reportes/reporte_usuarios_mes.html',ctx, context_instance = RequestContext(request)) 
    else:
        return HttpResponseRedirect('/')

def generar_pdf_usuarios_mes(request):
    #print "Genero el PDF"
    mes =0
    anio =0
    story =[]
    fecha_usuarios = x
    response = HttpResponse(content_type='application/pdf')
    pdf_name = "reporte_usuarios_mes.pdf"  # llamado clientes
    # la linea 26 es por si deseas descargar el pdf a tu computadora
    # response['Content-Disposition'] = 'attachment; filename=%s' % pdf_name
    

    buff = BytesIO()
    doc = SimpleDocTemplate(buff,
                            pagesize=letter,
                            rightMargin=40,
                            leftMargin=40,
                            topMargin=60,
                            bottomMargin=18,
                            )
    reportes = []
    styles = getSampleStyleSheet()
    fichero_imagen="biblioteca/media/images/Reports-banner.jpg" 

    imagen_logo=Image(os.path.realpath(fichero_imagen),width=400,height=100)
    story.append(imagen_logo)
    reportes.append(imagen_logo)




    header = Paragraph("Fecha del reporte: "+str(date.today()), styles['Heading1'])
    header2 = Paragraph("Reporte de los usuarios que prestaron libros en el mes "+str(fecha_usuarios.month)+" del "+str(fecha_usuarios.year), styles['Normal'])
    salto_linea = Paragraph("\n\n", styles["Normal"])





    reportes.append(Spacer(1, 12))
    reportes.append(header)
    #reportes.append(Spacer(1, 12))
    reportes.append(header2)
    reportes.append(Spacer(1, 12))


    
    headings = ('Fecha préstamo', 'Usuario', 'Nombre del libro', 'Fecha devolución')
    mes = x.month
    anio = x.year
    n = mes 
    f = mes

  

    
    allreportes = [(i.fecha_prestamo, i.usuario.nombre, i.libro.nombre_libro, i.fecha_devolucion) for i in Prestamo.objects.filter(fecha_prestamo__month =mes,fecha_prestamo__year = anio)]
    #print allreportes

    t = Table([headings] + allreportes)
    t.setStyle(TableStyle(
        [
            ('GRID', (0, 0), (3, -1), 1, colors.dodgerblue),
            ('LINEBELOW', (0, 0), (-1, 0), 2, colors.darkblue),
            ('BACKGROUND', (0, 0), (-1, 0), colors.dodgerblue)
        ]
    ))


    #GRAFICA DE BARRAS

    titulo1 = Paragraph("Gráfica comparativa de usuarios que prestaron libros en el mes "+str(fecha_usuarios.month)+" y el mes anterior a éste. ", estilo['title'])
    drawing = Drawing(400, 200)
    data = [(u1, u2)]
    bc = VerticalBarChart()
    bc.x = 50
    bc.y = 50
    bc.height = 125
    bc.width = 300
    bc.data = data
    bc.bars[0].fillColor = colors.blue
    bc.bars[1].fillColor = colors.red
    bc.strokeColor = colors.black
    bc.fillColor = colors.silver
    bc.valueAxis.valueMin = 0
    bc.valueAxis.valueMax = u2+10
    try:
        o = u2 / 2
        if type(o) == 'float':
            bc.valueAxis.valueStep = u2+0.5
        if type(o) == 'int':
            bc.valueAxis.valueStep = o

    except:
        "No se puede"


    bc.categoryAxis.labels.boxAnchor = 'ne'
    bc.categoryAxis.labels.dx = 8
    bc.categoryAxis.labels.dy = -2
    bc.categoryAxis.labels.angle = 0
    if mes == 1:
        n = mes + 11
    else:
        f = mes - 1 



    bc.categoryAxis.categoryNames = [ datetime.date(anio, f, 1).strftime('%B'), datetime.date(anio, n, 1).strftime('%B')]
    drawing.add(bc)

    bc.barLabels.nudge = 20
    bc.barLabelFormat = '%0.0f'
    bc.barLabels.dx = 0
    bc.barLabels.dy = 0
    bc.barLabels.boxAnchor = 'n' # irrelevant (becomes 'c')
    bc.barLabels.fontName = 'Helvetica'
    bc.barLabels.fontSize = 14

    



    reportes.append(t)
    reportes.append(Spacer(0, inch*.1))
    reportes.append(Spacer(0, inch*.1))
    reportes.append(titulo1)
    reportes.append(drawing)
    doc.build(reportes)
    response.write(buff.getvalue())
    buff.close()
    return response