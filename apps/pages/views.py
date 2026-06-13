from django.views.generic import TemplateView
from apps.core.mixins import ExtraCssMixin


class HomeView(ExtraCssMixin, TemplateView):
    template_name = 'pages/home.html'
    extra_css = [
        'css/components/hero.css',
        'css/components/cards.css',
        'css/components/glass.css',
        'css/components/buttons.css',
        'css/components/faq.css',
        'css/components/modal.css',
        'css/pages/home.css',
    ]

    def get_context_data(self, **kwargs):
        from django.utils.translation import gettext as _
        from apps.services.models import Service
        from apps.therapists.models import Therapist
        ctx = super().get_context_data(**kwargs)

        featured_therapists = list(
            Therapist.objects.filter(is_active=True).prefetch_related('specialties')[:6]
        )

        ctx['featured_services'] = Service.objects.filter(is_active=True)[:3]
        ctx['featured_therapists'] = featured_therapists
        ctx['process_steps'] = [
            {'num': '01', 'title': _('Vyberte masáž'), 'text': _('Prozkoumejte náš katalog masáží a vyberte typ, který nejlépe odpovídá vašim potřebám.')},
            {'num': '02', 'title': _('Zvolte masérku'), 'text': _('Každá z našich šesti masérky má jedinečnou specializaci. Vyberte tu, která vám vyhovuje.')},
            {'num': '03', 'title': _('Rezervujte termín'), 'text': _('V rozvrhu vyberte volný termín a potvrďte rezervaci. Potvrzení obdržíte e-mailem.')},
            {'num': '04', 'title': _('Relaxujte'), 'text': _('Přijďte 10 minut předem. Vše ostatní necháme na nás — váš čas je jen pro vás.')},
        ]
        ctx['faqs'] = [
            {'q': _('Jak se připravit na masáž?'), 'a': _('Před masáží doporučujeme přijít 10 minut předem, přijít čistí a hydratovaní. Vyhněte se jídlu hodinu před masáží.')},
            {'q': _('Jak rezervovat masáž?'), 'a': _('Rezervaci provedete online v sekci Rozvrh — vyberte masáž, zvolte masérku a volný termín.')},
            {'q': _('Jak dlouho masáž trvá?'), 'a': _('Délka masáže závisí na vybraném typu: od 60 minut (klasická, sportovní) do 90 minut (uvolňující).')},
            {'q': _('Jak probíhá platba?'), 'a': _('Přijímáme hotovost i platební karty. Platba probíhá na místě po skončení masáže.')},
            {'q': _('Nabízíte párovou masáž?'), 'a': _('Ano, párová masáž je možná po domluvě. Kontaktujte nás pro rezervaci pro dvě osoby.')},
            {'q': _('Co je zahrnuto v ceně?'), 'a': _('V ceně jsou masážní oleje, prostěradla a přístup do relaxační zóny.')},
        ]
        return ctx


class AboutView(ExtraCssMixin, TemplateView):
    template_name = 'pages/about.html'
    extra_css = [
        'css/components/glass.css',
        'css/components/buttons.css',
    ]


class SalonRulesView(ExtraCssMixin, TemplateView):
    template_name = 'pages/salon_rules.html'
    extra_css = ['css/components/glass.css']


class PrivacyView(ExtraCssMixin, TemplateView):
    template_name = 'pages/privacy.html'
    extra_css = ['css/components/glass.css']
