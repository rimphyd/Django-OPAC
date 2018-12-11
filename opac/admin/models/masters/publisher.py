from django.contrib import admin

from opac.models.masters.publisher import Publisher


class PublisherAdmin(admin.ModelAdmin):
    list_display = ('get_publisher_number', 'name', 'address')
    list_display_links = ('get_publisher_number', 'name')
    search_fields = ('name', 'address')

    def get_publisher_number(self, publisher):
        return publisher.id
    get_publisher_number.admin_order_field = 'id'
    get_publisher_number.short_description = '出版者番号'


admin.site.register(Publisher, PublisherAdmin)
