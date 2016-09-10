import re
from .models import Formulario
from django import forms

class FormFormularios(forms.ModelForm):

	class Meta:
		model = Formulario
		exclude = ['reporte', 'creacion']
		widgets = {
			'nombre':forms.TextInput(attrs={'class':'usuario', 'placeholder':'ingrese su nombre'}),
			'correo':forms.EmailInput(attrs={'class':'correo_usuario', 'placeholder':'ingrese su correo'}),
			'telefono':forms.TextInput(attrs={'class':'telefono', 'placeholder':'ingrese su telefono (####-####)'}),
			'servicio':forms.RadioSelect(attrs={'id':'value'})
		}

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

	def clean_telefono(self):
		telefono = self.cleaned_data['telefono']
		if not re.search(r'^(\d{4})-(\d{4})', telefono):
			self.add_error('telefono', 'ingrese un telefono de formtato ####-####')
		return telefono

