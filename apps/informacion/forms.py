import re
from django import forms
from .models import Publicacion

class FormPublicacion(forms.ModelForm):
	class Meta:
		model = Publicacion
		exclude = ['creacion']
		widgets = {
			'titulo':forms.TextInput(attrs={'class':'titulo', 'placeholder':'ingrese un titulo'}),
			'descripcion':forms.Textarea(attrs={'class':'descripcion', 'placeholder':'ingrese una descripcion'}),
			'archivo':forms.FileInput(attrs={'class':'archivo'})
		}

	def __init__(self, *args, **kwargs):
		super(FormPublicacion, self).__init__(*args, **kwargs)
		self.fields['titulo'].label = ''
		self.fields['descripcion'].label = ''
		self.fields['archivo'].label = ''

	def clean_titulo(self):
		titulo = self.cleaned_data['titulo']
		if len(titulo) < 8:
			self.add_error('titulo', 'debe agregar un titulo mas largo')
		return titulo

	def clean_descripcion(self):
		descripcion = self.cleaned_data['descripcion']
		if len(descripcion) > 200:
			self.add_error('descripcion', 'la descripcion no debe superar los 200 caracteres')
		return descripcion

	def clean_archivo(self):
		archivo = str(self.cleaned_data['archivo'])
		print archivo
		if not re.search(r'^.+(\.pdf)', archivo):
			self.add_error('archivo', 'los archivos deben ser extension pdf unicamente')
		return archivo

