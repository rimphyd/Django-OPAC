from django.contrib import admin

from opac.models.masters.translator import Translator


class TranslatorAdmin(admin.ModelAdmin):
    list_display = ('get_translator_number', 'name', 'get_translated_books')
    list_display_links = ('get_translator_number', 'name')
    search_fields = ('name', )
    exclude = ('books', )

    def get_translator_number(self, translator):
        return translator.id
    get_translator_number.admin_order_field = 'id'
    get_translator_number.short_description = '訳者番号'

    def get_translated_books(self, translator):
        return ', '.join(book.name for book in translator.books.all()[:5]) \
            or None
    get_translated_books.short_description = '訳書 (5冊まで)'


admin.site.register(Translator, TranslatorAdmin)
