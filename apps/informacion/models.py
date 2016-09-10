from __future__ import unicode_literals
from django.db import models
from django.db.models.signals import post_delete
from django.db import transaction
from django.dispatch import receiver

class Publicacion(models.Model):
	titulo = models.CharField(max_length=200, db_index=True)
	descripcion = models.TextField(blank=True, null=True)
	creacion = models.DateTimeField(auto_now_add=True)
	archivo = models.FileField(upload_to='publicaciones/')

	class Meta:
		ordering = ['id']
		verbose_name_plural = 'publicaciones'

	def __unicode__(self):
		return self.titulo

	def save(self, *args, **kwargs):
		try:
			with transaction.atomic():
				cambio = Publicacion.objects.get(id=self.id)
				if cambio.archivo != self.archivo:
					cambio.archivo.delete(save=True)
		except: pass         
		super(Publicacion, self).save(*args, **kwargs)

@receiver(post_delete, sender=Publicacion)
def borrar_archivo(sender, instance, **kwargs):
	instance.archivo.delete(False)
