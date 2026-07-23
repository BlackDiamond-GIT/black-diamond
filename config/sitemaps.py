from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from apps.blog.models import Article
from apps.services.models import Service


class BaseI18nSitemap(Sitemap):
    protocol = 'https'
    i18n = True
    alternates = True
    x_default = True
    languages = ('cs', 'en', 'ru')


class StaticViewSitemap(BaseI18nSitemap):
    changefreq = 'weekly'

    def items(self):
        return (
            'pages:home',
            'pages:about',
            'pages:salon_rules',
            'pages:privacy',
            'pages:prices',
            'pages:faq',
            'pages:contact',
            'services:list',
            'blog:list',
        )

    def location(self, item):
        return reverse(item)

    def priority(self, item):
        if item == 'pages:home':
            return 1.0
        if item in ('services:list', 'pages:contact'):
            return 0.9
        return 0.7


class ServiceSitemap(BaseI18nSitemap):
    changefreq = 'monthly'
    priority = 0.8

    def items(self):
        return Service.objects.filter(is_active=True).order_by('order', 'pk')

    def location(self, item):
        return reverse('services:detail', kwargs={'slug': item.slug})


class ArticleSitemap(BaseI18nSitemap):
    changefreq = 'monthly'
    priority = 0.6

    def items(self):
        return Article.objects.filter(is_published=True).order_by('-published_at')

    def location(self, item):
        return reverse('blog:detail', kwargs={'slug': item.slug})

    def lastmod(self, item):
        return item.published_at


SITEMAPS = {
    'static': StaticViewSitemap,
    'services': ServiceSitemap,
    'articles': ArticleSitemap,
}
