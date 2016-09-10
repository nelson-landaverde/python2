from django.contrib import admin
from .models import Publicacion
@admin.register(Publicacion)
class AdminPublicacion(admin.ModelAdmin):
	list_display = ['titulo', 'descripcion', 'creacion', 'archivo']
