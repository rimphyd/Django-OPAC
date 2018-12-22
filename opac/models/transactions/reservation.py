from django.db import models

from opac.models.abstracts import TimeStampedModel
from opac.models.masters.stock import Stock
from opac.models.masters.user import User


class Reservation(TimeStampedModel):
    class Meta:
        verbose_name = '予約'
        verbose_name_plural = '予約'
        unique_together = ('stock', 'user')

    stock = models.ForeignKey(
        Stock,
        verbose_name='蔵書',
        related_name='reservations',
        on_delete=models.PROTECT
    )
    user = models.ForeignKey(
        User,
        verbose_name='ユーザー',
        related_name='reservations',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f'{self.stock} : {self.user}'

    def order(self):
        return Reservation.objects \
            .filter(stock__id=self.stock.id) \
            .filter(created_at__lt=self.created_at) \
            .count() + 1
    order.short_description = '予約順位'
