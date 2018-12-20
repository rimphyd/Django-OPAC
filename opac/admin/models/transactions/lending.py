from logging import getLogger


from django.contrib import admin, messages
from django.utils import timezone

from opac.admin.messages import AdminMessage, LendingAdminMessage
from opac.models.transactions import Lending
from opac.services import LendingBackService, LendingRenewService, ServiceError

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
        if any(not l.is_renewable() for l in lendings):
            reasons = self._get_cant_renew_reasons(lendings)
            for reason in reasons:
                self.message_user(request, reason, level=messages.ERROR)
            return

        try:
            for lending in lendings:
                LendingRenewService(lending).exec()
        except ServiceError as e:
            logger.error('貸出データとエラー内容', e)
            self.message_user(
                request, AdminMessage.ERROR_OCCURRED, level=messages.ERROR)
        else:
            self.message_user(request, LendingAdminMessage.RENEWED)
    renew.short_description = '選択された 貸出 を延長する'

    def _get_cant_renew_reasons(self, lendings):
        reasons = []
        if any(l.is_renewed() for l in lendings):
            reasons.append(LendingAdminMessage.ALREADY_RENEWED)
        if any(l.stock.is_reserved() for l in lendings):
            reasons.append(LendingAdminMessage.RESERVATION_EXISTS)
        return reasons

    def back(self, request, lendings):
        try:
            for lending in lendings:
                LendingBackService(lending).exec()
        except ServiceError as e:
            logger.error('貸出データとエラー内容', e)
            self.message_user(
                request, AdminMessage.ERROR_OCCURRED, level=messages.ERROR)
        else:
            self.message_user(request, LendingAdminMessage.BACKED)
    back.short_description = '選択された 貸出 を返却する'


admin.site.register(Lending, LendingAdmin)
