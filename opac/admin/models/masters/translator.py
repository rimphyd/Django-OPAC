from django.contrib import admin
from django.utils.html import escape
from django.utils.safestring import mark_safe

from opac.models.masters.translator import Translator


class TranslatorAdmin(admin.ModelAdmin):
    list_display = ('get_translator_number', 'name', 'get_translated_books')
    list_display_links = ('get_translator_number', 'name')
    search_fields = ('name', )
    exclude = ('books', )

    def get_queryset(self, request):
        return Translator.objects.prefetch_related('books')

    def get_translator_number(self, translator):
        return translator.id
    get_translator_number.admin_order_field = 'id'
    get_translator_number.short_description = '訳者番号'

    @mark_safe
    def get_translated_books(self, translator):
        return '<br>'.join(
                   escape(b.name) for b in translator.books.all()[:5]
               ) \
            or '-'
    get_translated_books.short_description = '訳書 (5冊まで)'


admin.site.register(Translator, TranslatorAdmin)
