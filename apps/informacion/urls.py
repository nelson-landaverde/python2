from django.conf.urls import url 
from .views import *

urlpatterns = [
	url(r'^publicaciones/$', mostrar_publicacion_view.as_view(), name='publicaciones'),
	url(r'^adm_publicaciones/$', adm_publicacion.as_view(), name='adm_publicacion'),
	url(r'^generar_publicacion/$', publicacion_view.as_view(), name='generar_publicacion'),
	url(r'^modificar_publicacion/(?P<pk>\d+)/$', modificar_publicacion_view.as_view(), name='modificar_publicacion'),
	url(r'^eliminar_publicacion/(?P<pk>\d+)/$', eliminar_publicacion_view.as_view(), name='eliminar_publicacion'),
	url(r'^archivo_publicado/(?P<id>\d+)/$', ver_documento, name='ver_documento')
]