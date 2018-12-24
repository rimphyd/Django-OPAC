from logging import getLogger


from django.contrib import admin, messages
from django.utils import timezone

from opac.admin.messages import AdminMessage, LendingAdminMessage
from opac.models.transactions import Lending
from opac.services import LendingBackService, LendingRenewService, ServiceError
from opac.services.errors import (
    FirstReservationHoldingAlreadyExistsError,
    RenewingAlreadyExistsError,
    ReservationExistsError
)

logger = getLogger(__name__)


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
    actions = ('renew', 'back')

    def has_change_permission(self, request, obj=None):
        return False

    def get_queryset(self, request):
        return (
            Lending.objects
                   .prefetch_related('renewing')
                   .prefetch_related('stock__reservations')
        )

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
        return timezone.localtime(lending.created_at).date()
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

    def renew(self, request, lendings):
        try:
            for lending in lendings:
                LendingRenewService(lending).exec()
        except RenewingAlreadyExistsError as e:
            logger.warning('貸出の延長に失敗しました', e)
            self.message_user(
                request,
                LendingAdminMessage.RENEWING_ALREADY_EXISTS,
                level=messages.WARNING
            )
        except ReservationExistsError as e:
            logger.warning('貸出の延長に失敗しました', e)
            self.message_user(
                request,
                LendingAdminMessage.RESERVATION_EXISTS,
                level=messages.WARNING
            )
        except ServiceError as e:
            logger.exception('貸出の延長に失敗しました', e)
            self.message_user(
                request, AdminMessage.ERROR_OCCURRED, level=messages.ERROR)
        else:
            self.message_user(request, LendingAdminMessage.RENEWED)
    renew.short_description = '選択された 貸出 を延長する'

    def back(self, request, lendings):
        try:
            for lending in lendings:
                LendingBackService(lending).exec()
        except FirstReservationHoldingAlreadyExistsError as e:
            logger.exception('貸出の返却に失敗しました', e)
            self.message_user(
                request,
                LendingAdminMessage.FIRST_RESERVATION_HOLDING_ALREADY_EXISTS,
                level=messages.WARNING)
        except ServiceError as e:
            logger.exception('貸出の返却に失敗しました', e)
            self.message_user(
                request, AdminMessage.ERROR_OCCURRED, level=messages.ERROR)
        else:
            self.message_user(request, LendingAdminMessage.BACKED)
    back.short_description = '選択された 貸出 を返却する'


admin.site.register(Lending, LendingAdmin)
