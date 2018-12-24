from django.contrib import admin
from django.db.models import Count

from opac.models.masters.stock import Stock


class StockAdmin(admin.ModelAdmin):
    list_display = (
        'get_stock_number',
        'get_book_name',
        'get_book_isbn',
        'get_library_name',
        'get_lending_actual_due_date',
        'get_holding_expiration_date',
        'get_reservations_count'
    )
    list_filter = ('library__name', )
    search_fields = ('id', 'book__name', 'book__isbn')
    raw_id_fields = ('book', )

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(
            _reservations_count=Count('reservations')
        )
        return queryset

    def get_readonly_fields(self, request, obj=None):
        return ('book', ) if obj \
          else ()

    def get_stock_number(self, stock):
        return stock.id
    get_stock_number.admin_order_field = 'id'
    get_stock_number.short_description = '蔵書番号'

    def get_book_name(self, stock):
        return stock.book.name
    get_book_name.admin_order_field = 'book__name'
    get_book_name.short_description = '書名'

    def get_book_isbn(self, stock):
        return stock.book.isbn
    get_book_isbn.admin_order_field = 'book__isbn'
    get_book_isbn.short_description = 'ISBN'

    def get_library_name(self, stock):
        return stock.library.name
    get_library_name.admin_order_field = 'library__name'
    get_library_name.short_description = '館名'

    def get_lending_actual_due_date(self, stock):
        return stock.lending.actual_due_date()
    get_lending_actual_due_date.short_description = '返却期限 (延長含む)'

    def get_holding_expiration_date(self, stock):
        return stock.holding.expiration_date
    get_holding_expiration_date.admin_order_field = 'holding__expiration_date'
    get_holding_expiration_date.short_description = '取置期限'

    def get_reservations_count(self, stock):
        return stock._reservations_count
    get_reservations_count.admin_order_field = '_reservations_count'
    get_reservations_count.short_description = '予約数'


admin.site.register(Stock, StockAdmin)
