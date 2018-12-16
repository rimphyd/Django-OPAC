from django.contrib import admin
from django.utils.html import escape
from django.utils.safestring import mark_safe

from opac.models.masters.author import Author


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('get_author_number', 'name', 'get_authed_books')
    list_display_links = ('get_author_number', 'name')
    search_fields = ('name', )
    exclude = ('books', )

    def get_author_number(self, author):
        return author.id
    get_author_number.admin_order_field = 'id'
    get_author_number.short_description = '著者番号'

    @mark_safe
    def get_authed_books(self, author):
        return '<br>'.join(escape(b.name) for b in author.books.all()[:5]) \
            or '-'
    get_authed_books.short_description = '著書 (5冊まで)'


admin.site.register(Author, AuthorAdmin)
