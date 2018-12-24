from django.contrib import admin

from opac.models.transactions.renewing import Renewing


class RenewingAdmin(admin.ModelAdmin):
    list_display = (
        'get_renewing_number',
        'get_lending_number',
        'get_stock_number',
        'get_book_name',
        'get_user',
        'due_date'
    )
    search_fields = (
        'id',
        'lending__id',
        'lending__stock__id',
        'lending__stock__book__name',
        'lending__user__username'
    )
    raw_id_fields = ('lending', )

    def has_change_permission(self, request, obj=None):
        return False

    def get_renewing_number(self, renewing):
        return renewing.id
    get_renewing_number.admin_order_field = 'id'
    get_renewing_number.short_description = '延長番号'

    def get_lending_number(self, renewing):
        return renewing.lending.id
    get_lending_number.admin_order_field = 'lending__id'
    get_lending_number.short_description = '貸出番号'

    def get_stock_number(self, renewing):
        return renewing.lending.stock.id
    get_stock_number.admin_order_field = 'lending__stock__id'
    get_stock_number.short_description = '蔵書番号'

    def get_book_name(self, renewing):
        return renewing.lending.stock.book.name
    get_book_name.admin_order_field = 'lending__stock__book__name'
    get_book_name.short_description = '書名'

    def get_user(self, renewing):
        return renewing.lending.user
    get_user.admin_order_field = 'lending__user'
    get_user.short_description = 'ユーザー'


admin.site.register(Renewing, RenewingAdmin)
