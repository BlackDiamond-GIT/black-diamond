from django.test import TestCase

from apps.core.management.commands.seed_site import _rewrite_retired_service_links
from apps.core.models import SiteSettings
from apps.core.seed_data_services import SERVICES


class PublicCompanyDetailsTests(TestCase):
    def test_site_settings_defaults_use_requested_contact(self):
        site = SiteSettings.load()

        self.assertEqual(site.address, 'Opletalova 1566/30, 110 00 Praha')
        self.assertEqual(site.phone_primary, '+420 778 622 334')
        self.assertEqual(site.whatsapp_number, '420778622334')
        self.assertEqual(site.get_rotation_phones(), ['+420 778 622 334'] * 3)

    def test_homepage_has_requested_seo_and_legal_disclaimer(self):
        response = self.client.get('/cs/')

        self.assertContains(response, '<title>Black Diamond Spa | Luxusní relaxační masáže Praha</title>', html=True)
        self.assertContains(response, 'Prémiový masážní salon v centru Prahy na adrese Opletalova 30.')
        self.assertContains(response, 'Provozovatelem salonu Black Diamond Spa je společnost Prague relax s.r.o.')
        self.assertContains(response, 'Black Diamond Spa je registrovaná ochranná známka.')

        english = self.client.get('/en/')
        russian = self.client.get('/ru/')
        self.assertContains(english, 'The operator of Black Diamond Spa is Prague relax s.r.o.')
        self.assertContains(english, 'All our services are provided by certified staff')
        self.assertContains(russian, 'Оператором салона Black Diamond Spa является компания Prague relax s.r.o.')
        self.assertContains(russian, 'Все наши услуги предоставляются сертифицированным персоналом')

    def test_contact_and_privacy_show_legal_operator(self):
        contact = self.client.get('/cs/kontakty/')
        privacy = self.client.get('/cs/soukromi/')

        for response in (contact, privacy):
            self.assertContains(response, 'Prague relax s.r.o.')
            self.assertContains(response, '23481412')
            self.assertContains(response, 'Chvalská 718/10, Hloubětín, 198 00 Praha 9')
        self.assertContains(contact, 'Opletalova 1566/30')
        self.assertContains(contact, '+420 778 622 334')

    def test_seed_has_requested_localized_service_summaries(self):
        by_slug = {service['slug']: service for service in SERVICES}

        self.assertEqual(
            by_slug['vip-masaz']['short_cs'],
            'Exkluzivní a individuální celotělová péče s plnou pozorností certifikovaného terapeuta za využití prémiových bio olejů.',
        )
        self.assertIn('certified therapist', by_slug['vip-masaz']['short_en'])
        self.assertIn('сертифицированного терапевта', by_slug['vip-masaz']['short_ru'])
        self.assertEqual(
            by_slug['masaz-pro-zeny']['short_cs'],
            'Zklidňující regenerační rituál v harmonickém a plně soukromém prostředí, zaměřený na odbourání stresu a hluboké uvolnění svalů.',
        )


class PublicRoutingAndSeoTests(TestCase):
    def test_therapist_detail_redirect_ignores_slug_in_every_language(self):
        for language in ('cs', 'en', 'ru'):
            response = self.client.get(f'/{language}/masazistky/julia/')
            self.assertRedirects(
                response,
                f'/{language}/',
                fetch_redirect_response=False,
            )

    def test_retired_services_redirect_to_active_service_in_every_language(self):
        retired_slugs = (
            'aromaterapie',
            'cbd-relaxacni-masaz',
            'klasicka-masaz',
            'lymfaticka-masaz',
        )
        for language in ('cs', 'en', 'ru'):
            for retired_slug in retired_slugs:
                response = self.client.get(
                    f'/{language}/masaze/{retired_slug}/'
                )
                self.assertRedirects(
                    response,
                    f'/{language}/masaze/relaxacni-masaz/',
                    status_code=301,
                    fetch_redirect_response=False,
                )

    def test_seed_rewrites_retired_service_links(self):
        content = (
            '<a href="/cs/masaze/aromaterapie/">Aroma</a>'
            '<a href="/en/masaze/lymfaticka-masaz/">Lymphatic</a>'
        )
        rewritten = _rewrite_retired_service_links(content)
        self.assertNotIn('/masaze/aromaterapie/', rewritten)
        self.assertNotIn('/masaze/lymfaticka-masaz/', rewritten)
        self.assertEqual(rewritten.count('/masaze/relaxacni-masaz/'), 2)

    def test_robots_and_sitemap_are_public_and_multilingual(self):
        robots = self.client.get('/robots.txt')
        self.assertEqual(robots.status_code, 200)
        self.assertEqual(robots['Content-Type'], 'text/plain; charset=utf-8')
        self.assertContains(
            robots,
            'Sitemap: https://black-diamond.cz/sitemap.xml',
        )

        sitemap_response = self.client.get('/sitemap.xml')
        self.assertEqual(sitemap_response.status_code, 200)
        self.assertIn('application/xml', sitemap_response['Content-Type'])
        sitemap_xml = sitemap_response.content.decode()
        for language in ('cs', 'en', 'ru'):
            self.assertIn(f'https://testserver/{language}/', sitemap_xml)
        self.assertNotIn('aromaterapie', sitemap_xml)

    def test_canonical_and_hreflang_use_the_live_domain_in_every_language(self):
        for language in ('cs', 'en', 'ru'):
            response = self.client.get(f'/{language}/')
            self.assertEqual(response.status_code, 200)
            self.assertContains(
                response,
                f'<link rel="canonical" href="https://black-diamond.cz/{language}/">',
                html=True,
            )
            self.assertNotContains(response, 'https://blackdiamond.cz')
