from django.conf.urls import url
from .views import *
urlpatterns = [
	url(r'^solicitud_formulario/$', form_view.as_view(), name='formulario'),
	url(r'^administracion_formularios/$', backend_form_view.as_view(), name='backend_form'),
	url(r'^detalle_reporte/(?P<id>\d+)/$', detalle_reporte, name='detalle'),
	url(r'^borrar_registro/(?P<pk>\d+)/$', delete_view.as_view(), name='delete'),
]