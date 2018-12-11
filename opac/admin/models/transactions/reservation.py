from django.contrib import admin

from opac.models.transactions.reservation import Reservation


class ReservationAdmin(admin.ModelAdmin):
    list_display = (
        'get_reservation_number',
        'get_stock_number',
        'get_book_name',
        'user',
        'get_reserved_at',
        'order'
    )
    search_fields = ('id', 'stock__id', 'stock__book__name', 'user__username')
    raw_id_fields = ('stock', 'user')

    def has_change_permission(self, request, obj=None):
        return False

    def get_reservation_number(self, reservation):
        return reservation.id
    get_reservation_number.admin_order_field = 'id'
    get_reservation_number.short_description = '予約番号'

    def get_stock_number(self, reservation):
        return reservation.stock.id
    get_stock_number.admin_order_field = 'stock__id'
    get_stock_number.short_description = '蔵書番号'

    def get_book_name(self, reservation):
        return reservation.stock.book.name
    get_book_name.admin_order_field = 'stock__book__id'
    get_book_name.short_description = '書名'

    def get_reserved_at(self, reservation):
        return reservation.created_at
    get_reserved_at.admin_order_field = 'created_at'
    get_reserved_at.short_description = '予約日時'


admin.site.register(Reservation, ReservationAdmin)
