from logging import getLogger

from django.contrib import admin, messages
from django.utils import timezone

from opac.admin.messages import AdminMessage, HoldingAdminMessage
from opac.models.transactions import Holding
from opac.services import (
    FirstReservationHoldingAlreadyExistsError,
    LendingAlreadyExistsError,
    ServiceError
)
from opac.services.holding import HoldingCancelService, HoldingLendService

logger = getLogger(__name__)


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
    actions = ('lend', 'cancel')

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
        return timezone.localtime(holding.created_at).date()
    get_held_at.admin_order_field = 'created_at'
    get_held_at.short_description = '取置日'

    def get_is_not_expired(self, holding):
        return not holding.is_expired()
    get_is_not_expired.admin_order_field = 'expiration_date'
    get_is_not_expired.boolean = True
    get_is_not_expired.short_description = '有効期限内？'

    def lend(self, request, holdings):
        try:
            for holding in holdings:
                HoldingLendService(holding).exec()
        except LendingAlreadyExistsError as e:
            logger.warning('取置の貸出に失敗しました', e)
            self.message_user(
                request,
                HoldingAdminMessage.LENDING_ALREADY_EXISTS,
                level=messages.WARNING
            )
        except ServiceError as e:
            logger.exception('取置の貸出に失敗しました', e)
            self.message_user(
                request, AdminMessage.ERROR_OCCURRED, level=messages.ERROR)
        else:
            self.message_user(request, HoldingAdminMessage.LENT)
    lend.short_description = '選択された 取置 を貸出にする'

    def cancel(self, request, holdings):
        try:
            for holding in holdings:
                HoldingCancelService(holding).exec()
        except FirstReservationHoldingAlreadyExistsError as e:
            logger.exception('取置の取り消しに失敗しました', e)
            self.message_user(
                request,
                HoldingAdminMessage.FIRST_RESERVATION_HOLDING_ALREADY_EXISTS,
                level=messages.WARNING
            )
        except ServiceError as e:
            logger.exception('取置の取り消しに失敗しました', e)
            self.message_user(
                request, AdminMessage.ERROR_OCCURRED, level=messages.ERROR)
        else:
            self.message_user(request, HoldingAdminMessage.CANCELED)
    cancel.short_description = '選択された 取置 を取り消す'


admin.site.register(Holding, HoldingAdmin)
