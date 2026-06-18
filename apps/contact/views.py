from django.conf import settings
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView
from apps.core.mixins import ExtraCssMixin
from .forms import ContactForm
from .models import ContactRequest


class ContactPageView(ExtraCssMixin, TemplateView):
    template_name = 'contact/index.html'
    extra_css = [
        'css/components/forms.css',
        'css/components/glass.css',
        'css/components/buttons.css',
        'css/pages/contact.css',
    ]

    def get_context_data(self, **kwargs):
        from apps.services.models import Service
        ctx = super().get_context_data(**kwargs)
        ctx['form'] = ContactForm()
        ctx['services'] = Service.objects.filter(is_active=True)
        return ctx


def contact_submit(request):
    """
    HTMX-ендпоінт для форми контакту.
    Повертає HTML-фрагмент: успіх або помилки валідації.
    """
    if request.method != 'POST':
        return HttpResponse(status=405)

    form = ContactForm(request.POST)

    if not form.is_valid():
        return render(request, 'contact/_form_errors.html', {'form': form}, status=422)

    contact: ContactRequest = form.save()

    try:
        send_mail(
            subject=f'[Black Diamond Spa] Новий запит від {contact.name}',
            message=(
                f'Ім\'я: {contact.name}\n'
                f'Email: {contact.email}\n'
                f'Телефон: {contact.phone}\n'
                f'Послуга: {contact.service}\n\n'
                f'{contact.message}'
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.CONTACT_RECIPIENT_EMAIL],
            fail_silently=True,
        )
    except Exception:
        pass

    return render(request, 'contact/_form_success.html', {'contact': contact})
