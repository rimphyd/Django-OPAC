from django.db import models
from django.utils import timezone

from opac.models.abstracts import TimeStampedModel
from opac.models.masters.stock import Stock
from opac.models.masters.user import User


class Lending(TimeStampedModel):
    class Meta:
        verbose_name = '貸出'
        verbose_name_plural = '貸出'

    stock = models.OneToOneField(
        Stock,
        verbose_name='蔵書',
        related_name='lending',
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        User,
        verbose_name='ユーザー',
        related_name='lendings',
        on_delete=models.PROTECT
    )
    due_date = models.DateField(
        '返却期限'
    )

    def __str__(self):
        return '{} : {}'.format(self.stock, self.user)

    def actual_due_date(self):
        return self.renewing.due_date if self.is_renewed() \
          else self.due_date

    def is_renewed(self):
        return hasattr(self, 'renewing')

    def is_overdue(self):
        return self.actual_due_date() < timezone.localdate()

    def is_renewable(self):
        return not self.is_renewed() \
           and not self.stock.is_reserved()
    is_renewable.boolean = True
    is_renewable.short_description = '延長可能？'
