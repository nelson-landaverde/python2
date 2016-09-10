from django.conf.urls import url, include
from .views import *
urlpatterns = [
	url(r'^inicio/$', inicio_view.as_view(), name='inicio'),
	url(r'^adm_backend/$', backend_view.as_view(), name='backend'),
	url(r'^', include('apps.formulario.urls')),
	url(r'^', include('apps.informacion.urls')),
	url(r'^contacto/$', contacto_view.as_view(), name='contacto')
]