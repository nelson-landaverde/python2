from .forms import FormContacto
from django.conf import settings
from django.core.mail import EmailMessage
from django.views import generic
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

class inicio_view(generic.TemplateView):
	template_name = 'inicio.html'

class backend_view(generic.TemplateView):
	template_name = 'backend.html'

	def get(self, request, *args, **kwargs):
		admin = request.user
		if not admin.is_superuser and not admin.is_authenticated():
			return HttpResponseRedirect('inicio/pagina')
		return super(backend_view, self).get(request, *args, **kwargs)

class contacto_view(generic.FormView):
	form_class = FormContacto
	template_name = 'contacto.html'

	def form_valid(self, form):
		email = EmailMessage(
				form.cleaned_data['nombre'] + '  ' + form.cleaned_data['correo'],
				form.cleaned_data['mensaje'],
				form.cleaned_data['correo'],
				['{}'.format(settings.EMAIL_HOST_USER)]
			)
		email.send()
		return super(contacto_view, self).form_valid(form)

	def get_success_url(self):
		return reverse('principal:contacto')



