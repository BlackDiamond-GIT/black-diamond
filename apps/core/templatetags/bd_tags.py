from django import template
from django.utils.translation import get_language

from apps.core.pricing import build_price_display

register = template.Library()


@register.filter
def trans_field(obj, field_base):
    """
    Повертає поле моделі відповідно до поточної мови.
    Використання: {{ service|trans_field:"title" }}
    """
    lang = get_language() or 'cs'
    lang_code = lang[:2]
    field_name = f'{field_base}_{lang_code}'
    fallback = f'{field_base}_cs'
    value = getattr(obj, field_name, None)
    if not value:
        value = getattr(obj, fallback, '')
    return value


@register.simple_tag
def asset_img(category, slug, ext='webp'):
    """Статичне зображення за slug: img/{category}/{slug}.{ext}"""
    from django.templatetags.static import static
    return static(f'img/{category}/{slug}.{ext}')


@register.filter
def faq_items(obj):
    lang = get_language() or 'cs'
    return obj.get_faq(lang[:2])


@register.filter
def price_plain(amount_czk):
    """Plain-text multi-currency price for selects and meta."""
    from apps.core.pricing import CurrencySettings, format_price_plain
    return format_price_plain(amount_czk, CurrencySettings())


@register.simple_tag(takes_context=True)
def price_plain_tag(context, amount_czk):
    from apps.core.pricing import CurrencySettings, format_price_plain
    currency = context.get('currency_settings') or CurrencySettings()
    return format_price_plain(amount_czk, currency)


@register.inclusion_tag('includes/_price_multi.html', takes_context=True)
def price_multi(context, amount_czk, compact=False, class_name=''):
    currency = context.get('currency_settings')
    if currency is None:
        from apps.core.pricing import CurrencySettings
        currency = CurrencySettings()
    price = build_price_display(amount_czk, currency)
    return {
        'price': price,
        'compact': compact,
        'class': class_name,
    }


@register.simple_tag(takes_context=True)
def lang_url(context, lang_code):
    """
    Повертає URL поточної сторінки для вказаної мови.
    Використання: {% lang_url "en" %}
    """
    request = context.get('request')
    if not request:
        return f'/{lang_code}/'
    path = request.path
    current_lang = get_language() or 'cs'
    current_prefix = f'/{current_lang[:2]}/'
    if path.startswith(current_prefix):
        return f'/{lang_code}/' + path[len(current_prefix):]
    return f'/{lang_code}/'
