from django.contrib import admin
from .models import Category, Article
from modeltranslation.admin import TranslationAdmin
from django.utils.safestring import mark_safe

admin.site.site_header = 'News.am Administration'


@admin.register(Category)
class CategoryAdmin(TranslationAdmin):
    list_display = ('id', 'title')
    list_display_links = ('id', 'title')
    search_fields = ('title',)


@admin.register(Article)
class ArticleAdmin(TranslationAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('id', 'title', 'category', 'date', 'status', 'image',)
    list_display_links = ('id', 'title')
    list_filter = ('category__title', 'date', 'author', 'status', 'image',)
    search_fields = ('title', 'author', 'category__title',)
    # readonly_fields = ('image',)
    save_on_top = True
    list_editable = ('status', 'date')


fieldsets = (
    ('Categories', {
        'fields': (('category', 'additional_category'),)
    }),
    ('Title and Slug', {
        'fields': (('title', 'slug'),)
    }),
    ('Author and Status', {
        'fields': (('author', 'status'),)
    }),
    ('Content', {
        'fields': ('content',)
    }),
    ('Date and Picture', {
        'fields': ('image',)
    }),
    ('', {
        'fields': ('date',)
    }),
)


def get_image(self, obj):
    return mark_safe(f'<img src={obj.picture.url} width="90" height="70"')


get_image.short_description = 'Picture'
