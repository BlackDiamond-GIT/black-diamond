class ExtraCssMixin:
    """
    Додає список CSS-файлів до контексту шаблону.
    Використовується в TemplateView для підключення компонентних CSS.
    """
    extra_css = []

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['extra_css'] = self.extra_css
        return ctx


class HtmxMixin:
    """
    Визначає, чи запит прийшов через HTMX.
    Якщо так — повертає partial template (без base.html).
    """
    htmx_template = None

    def get_template_names(self):
        if self.request.headers.get('HX-Request') and self.htmx_template:
            return [self.htmx_template]
        return super().get_template_names()
