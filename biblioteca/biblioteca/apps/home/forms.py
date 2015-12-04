from django import forms

from django.forms.extras import SelectDateWidget
from django.contrib.admin import widgets


class espacionuevo_form(forms.Form):

	fecha_inicio = forms.DateField(widget = forms.TextInput(attrs={'id':'datepicker'}), label='fecha_inicio')

class Login_form(forms.Form):
	usuario 	= forms.CharField(widget = forms.TextInput())
	clave		= forms.CharField(widget = forms.PasswordInput(render_value = False))

class contact_form(forms.Form):
	
	correo = forms.EmailField(widget = forms.TextInput())
	titulo = forms.CharField(widget = forms.TextInput())
	texto  = forms.CharField(widget = forms.Textarea()) 