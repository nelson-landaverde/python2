import re
from django import forms

class FormContacto(forms.Form):
	nombre = forms.CharField(max_length=100, label='')
	correo = forms.EmailField(required=True, label='')
	mensaje = forms.CharField(max_length=500, label='')

	def __init__(self, *args, **kwargs):
		super(FormContacto, self).__init__(*args, **kwargs)
		self.fields['nombre'].widget = forms.TextInput(attrs={'class':'nombre_contacto', 'placeholder':'ingrese su nombre'})
		self.fields['correo'].widget = forms.EmailInput(attrs={'class':'correo_contacto', 'placeholder':'ingrese su correo'})
		self.fields['mensaje'].widget = forms.Textarea(attrs={'class':'mensaje_contacto', 'placeholder':'ingrese un mensaje'})

	def clean_nombre(self):
		nombre = self.cleaned_data['nombre']
		if not re.search(r'^([a-z]+)\s([a-z]+)\s*?([a-z]+)\s*?([a-z]+)\s*?$', nombre, re.I):
			self.add_error('nombre', 'ingrese su nombre completo')
		return nombre

	def clean_correo(self):
		correo = self.cleaned_data['correo']
		if not re.search(r'^.+@(hotmail|gmail|yahoo|outlook)\.(com|es)$', correo):
			self.add_error('correo', 'ingrese un correo valido')
		return correo
