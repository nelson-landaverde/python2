from __future__ import unicode_literals
from django.db import models
from django.conf import settings
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from django.core.mail import EmailMessage

class Formulario(models.Model):
	servicios = (
	('Auditor', 'auditor'),
	('Consultor', 'consultor'),
	('Finanza', 'finanza'),
	('Contable', 'contable')
	)
	nombre = models.CharField(max_length=200, db_index=True)
	correo = models.EmailField(db_index=True, unique=False)
	telefono = models.CharField(max_length=9)
	servicio = models.CharField(max_length=300, choices=servicios, default='')
	creacion = models.DateTimeField(auto_now_add=True)
	reporte  = models.FileField(upload_to='reportes/')

	class Meta:
		ordering = ['id']
		verbose_name_plural = 'formulario_de_registros'

	def __unicode__(self):
		return self.correo

@receiver(post_delete, sender=Formulario)
def eliminar_reporte(sender, instance, **kwargs):
	instance.reporte.delete(False)

@receiver(post_save, sender=Formulario)
def enviar_correo(sender, instance, **kwargs):
	email = EmailMessage(
			'hola administrado',
			'revise el sistema para ver nuevos registros',
			'{}'.format(instance.correo),
			['{}'.format(settings.EMAIL_HOST_USER)]
		)
	email.attach( str(instance.reporte), instance.reporte.read(), 'application/pdf' )
	email.send()

