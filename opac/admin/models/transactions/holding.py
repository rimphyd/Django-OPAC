from django.contrib import admin

from opac.models.transactions.holding import Holding


class HoldingAdmin(admin.ModelAdmin):
    list_display = (
        'get_holding_number',
        'get_stock_number',
        'get_book_name',
        'user',
        'get_held_at',
        'expiration_date',
        'get_is_not_expired'
    )
    search_fields = ('id', 'stock__id', 'stock__book__name', 'user__username')
    raw_id_fields = ('stock', 'user')

    def has_change_permission(self, request, obj=None):
        return False

    def get_holding_number(self, holding):
        return holding.id
    get_holding_number.admin_order_field = 'id'
    get_holding_number.short_description = '取置番号'

    def get_stock_number(self, holding):
        return holding.stock.id
    get_stock_number.admin_order_field = 'stock__id'
    get_stock_number.short_description = '蔵書番号'

    def get_book_name(self, holding):
        return holding.stock.book.name
    get_book_name.admin_order_field = 'stock__book__name'
    get_book_name.short_description = '書名'

    def get_held_at(self, holding):
        return holding.created_at.date()
    get_held_at.admin_order_field = 'created_at'
    get_held_at.short_description = '取置日'

    def get_is_not_expired(self, holding):
        return not holding.is_expired()
    get_is_not_expired.admin_order_field = 'expiration_date'
    get_is_not_expired.boolean = True
    get_is_not_expired.short_description = '有効期限内？'


admin.site.register(Holding, HoldingAdmin)
