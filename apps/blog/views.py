from django.views.generic import ListView, DetailView
from apps.core.mixins import ExtraCssMixin
from .models import Article


class ArticleListView(ExtraCssMixin, ListView):
    model = Article
    template_name = 'blog/list.html'
    context_object_name = 'articles'
    queryset = Article.objects.filter(is_published=True)
    paginate_by = 9
    extra_css = [
        'css/components/cards.css',
        'css/components/glass.css',
        'css/pages/blog.css',
    ]


class ArticleDetailView(ExtraCssMixin, DetailView):
    model = Article
    template_name = 'blog/detail.html'
    context_object_name = 'article'
    extra_css = [
        'css/components/glass.css',
        'css/components/buttons.css',
        'css/pages/blog.css',
    ]

    def get_queryset(self):
        return Article.objects.filter(is_published=True)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['related'] = Article.objects.filter(is_published=True).exclude(
            pk=self.object.pk
        )[:3]
        return ctx
