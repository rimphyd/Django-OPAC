from django.contrib import admin

from opac.models.masters.library import Library


class LibraryAdmin(admin.ModelAdmin):
    list_display = ('get_library_number', 'name', 'address')
    list_display_links = ('get_library_number', 'name')
    search_fields = ('name', 'address')

    def get_library_number(self, library):
        return library.id
    get_library_number.admin_order_field = 'id'
    get_library_number.short_description = '図書館番号'


admin.site.register(Library, LibraryAdmin)
