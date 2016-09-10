from datetime import date
from .models import Formulario
from .forms import FormFormularios
from .archivopdf import generar_reporte
from django.shortcuts import get_object_or_404
from django.views import generic
from django.contrib import messages
from django.db.models import Q
from django.core.files.base import ContentFile
from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponseRedirect, HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

class form_view(generic.FormView):
	form_class = FormFormularios
	template_name = 'formulario.html'

	def form_valid(self, form):
		instance = [form.cleaned_data['nombre'],form.cleaned_data['correo'],
					form.cleaned_data['telefono'],form.cleaned_data['servicio'], date.today()]
		form.instance.reporte.save(instance[1] + '.pdf',
		ContentFile( generar_reporte('archivos/reportes.html', {'instance':instance} )))
		messages.success(self.request, 'solicitud enviada con exito, se mantendra en contacto con usted.')
		return super(form_view, self).form_valid(form)

	def get_success_url(self):
		return reverse('principal:formulario')


class backend_form_view(generic.ListView):
	model = Formulario
	paginate_by = 3
	template_name = 'backend_form.html'

	def get(self, request, *args, **kwargs):
		admin = request.user 
		if not admin.is_superuser and not admin.is_authenticated():
			return HttpResponseRedirect('/pagina/inicio/')
		return super(backend_form_view, self).get(request, *args, **kwargs)

	def get_queryset(self):
		queryset = self.request.GET.get('q')
		if queryset:
			try: 
				render = Formulario.objects.filter( Q(nombre__icontains=queryset) | Q(correo__icontains=queryset) )
				return render
			except:
				return 'no existe la busqueda que desea'
		return super(backend_form_view, self).get_queryset()

		def get_context_data(self, **kwargs):
			context = super(backend_view, self).get_context_data(**kwargs) 
			formulario = Formulario.objects.all()
			paginador = Paginator(formulario, self.paginate_by)
			pagina = self.request.GET.get('page')
			try:
			    archivo = paginador.page(pagina)
			except PageNotAnInteger:
			    archivo = paginador.page(1)
			except EmptyPage:
			    archivo = paginador.page(paginador.num_pages)
			context['list_exams'] = archivo
			return context


def detalle_reporte(request, id):
	admin = request.user
	if not admin.is_superuser and not admin.is_authenticated():
		return HttpResponseRedirect('/pagina/inicio/')
	else:
		detalle = get_object_or_404(Formulario, id=id)
		return generar_reporte('archivos/detalle.html', {'instance':detalle})


class delete_view(generic.DeleteView):
	model = Formulario
	context_object_name = 'form'
	template_name = 'eliminar_reporte.html'

	def get_success_url(self):
		return reverse_lazy('principal:backend_form')



