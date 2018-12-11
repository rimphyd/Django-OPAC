from django.contrib import admin

from opac.models.transactions.lending import Lending


class LendingAdmin(admin.ModelAdmin):
    list_display = (
        'get_lending_number',
        'get_stock_number',
        'get_book_name',
        'user',
        'get_lent_at',
        'due_date',
        'get_renewed_due_date',
        'get_is_not_overdue',
        'get_is_stock_reserved',
        'get_is_renewed',
        'is_renewable'
    )
    search_fields = ('id', 'stock__id', 'stock__book__name', 'user__username')
    raw_id_fields = ('stock', 'user')

    def has_change_permission(self, request, obj=None):
        return False

    def get_lending_number(self, lending):
        return lending.id
    get_lending_number.admin_order_field = 'id'
    get_lending_number.short_description = '貸出番号'

    def get_stock_number(self, lending):
        return lending.stock.id
    get_stock_number.admin_order_field = 'stock__id'
    get_stock_number.short_description = '蔵書番号'

    def get_book_name(self, lending):
        return lending.stock.book.name
    get_book_name.admin_order_field = 'stock__book__name'
    get_book_name.short_description = '書名'

    def get_lent_at(self, lending):
        return lending.created_at.date()
    get_lent_at.admin_order_field = 'created_at'
    get_lent_at.short_description = '貸出日'

    def get_renewed_due_date(self, lending):
        return lending.renewing.due_date
    get_renewed_due_date.admin_order_field = 'renewing__due_date'
    get_renewed_due_date.short_description = '延長期限'

    def get_is_not_overdue(self, lending):
        return not lending.is_overdue()
    get_is_not_overdue.boolean = True
    get_is_not_overdue.short_description = '返却期限内？'

    def get_is_stock_reserved(self, lending):
        return 'Yes' if lending.stock.is_reserved() else 'No'
    get_is_stock_reserved.short_description = '予約有り？'

    def get_is_renewed(self, lending):
        return 'Yes' if lending.is_renewed() else 'No'
    get_is_renewed.short_description = '延長済み？'


admin.site.register(Lending, LendingAdmin)
