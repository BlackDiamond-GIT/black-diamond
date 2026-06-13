from django.contrib import admin
from .models import Article


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title_cs', 'published_at', 'is_published')
    list_editable = ('is_published',)
    list_filter = ('is_published',)
    prepopulated_fields = {'slug': ('title_cs',)}
    search_fields = ('title_cs', 'title_en')
    date_hierarchy = 'published_at'
