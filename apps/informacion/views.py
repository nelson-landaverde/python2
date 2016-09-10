from .models import Publicacion
from .forms import FormPublicacion
from django.views import generic
from django.conf import settings
from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import get_object_or_404
from django.core.files.base import ContentFile
from django.core.urlresolvers import reverse, reverse_lazy

def ver_documento(request, id):
	documento = get_object_or_404(Publicacion, id=id)
	archivo = settings.MEDIA_ROOT 
	with open(archivo + '/{}'.format(documento.archivo.name), 'rb') as file:
		response = HttpResponse(file.read(), content_type='application/pdf')
		response['Content-Disposition'] = 'filename=some_file.pdf'
		return response
	file.closed

class publicacion_view(generic.FormView):
	form_class = FormPublicacion
	template_name = 'generar_publicacion.html'

	def form_valid(self, form):
		form.instance.archivo = self.request.FILES['archivo']
		form.save()
		return super(publicacion_view, self).form_valid(form)

	def get(self, request, *args, **kwargs):
		admin = request.user 
		if not admin.is_superuser and not admin.is_authenticated():
			return HttpResponseRedirect('/pagina/publicaciones/')
		return super(publicacion_view, self).get(request, *args, **kwargs)

	def get_success_url(self):
		return reverse('principal:publicaciones')

class modificar_publicacion_view(generic.UpdateView):
	model = Publicacion
	form_class = FormPublicacion
	template_name = 'actualizar_publicacion.html'

	def get(self, request, *args, **kwargs):
		admin = request.user 
		if not admin.is_superuser and not admin.is_authenticated():
			return HttpResponseRedirect('/pagina/adm_publicaciones/')
		return super(modificar_publicacion_view, self).get(request, *args, **kwargs)

	def form_valid(self, form):
		form.instance.archivo = self.request.FILES['archivo']
		form.save()
		return super(modificar_publicacion_view, self).form_valid(form)

	def get_success_url(self):
		return reverse_lazy('principal:publicaciones')

class eliminar_publicacion_view(generic.DeleteView):
	model = Publicacion
	context_object_name = 'form'
	template_name = 'eliminar_publicacion.html'

	def get(self, request, *args, **kwargs):
		admin = request.user 
		if not admin.is_superuser and not admin.is_authenticated():
			return HttpResponseRedirect('/pagina/publicaciones/')
		return super(eliminar_publicacion_view, self).get(request, *args, **kwargs)

	def get_success_url(self):
		return reverse_lazy('principal:publicaciones')

class mostrar_publicacion_view(generic.ListView):
	model = Publicacion
	paginate_by = 3
	template_name = 'mostrar_publicacion.html'

	def get_queryset(self):
		queryset = self.request.GET.get('q')
		if queryset:
			try:
				render = Publicacion.objects.filter( Q(titulo=queryset) )
				return render
			except:
				return HttpResponse('<h3>no existe la busqueda deseada </h3>')
		return super(mostrar_publicacion_view, self).get_queryset()

	def get_context_data(self, **kwargs):
		context = super(mostrar_publicacion_view, self).get_context_data(**kwargs) 
		publicacion = Publicacion.objects.all()
		paginador = Paginator(publicacion, self.paginate_by)
		pagina = self.request.GET.get('page')
		try:
		    archivo = paginador.page(pagina)
		except PageNotAnInteger:
		    archivo = paginador.page(1)
		except EmptyPage:
		    archivo = paginador.page(paginador.num_pages)
		context['list_exams'] = archivo
		return context

class adm_publicacion(mostrar_publicacion_view):
	template_name = 'backend_public.html'

	def get(self, request, *args, **kwargs):
		admin = request.user
		if not admin.is_superuser and not admin.is_authenticated():
			return HttpResponseRedirect('/pagina/inicio/')
		return super(adm_publicacion, self).get(request, *args, **kwargs)