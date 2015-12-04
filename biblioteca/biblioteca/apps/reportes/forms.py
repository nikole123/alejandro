from django import forms



class fecha_mes_form(forms.Form):
	fecha = forms.DateField(widget = forms.TextInput(attrs={'id':'datepicker'}), label='fecha')
