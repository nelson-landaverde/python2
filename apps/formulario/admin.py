from django.contrib import admin
from .models import Formulario
@admin.register(Formulario)
class AdminFormularios(admin.ModelAdmin):
	list_display = ['nombre', 'correo', 'telefono', 'servicio', 'reporte']
