from django.db import models
from django.utils import timezone

from opac.models.abstracts import TimeStampedModel
from opac.models.masters.stock import Stock
from opac.models.masters.user import User


class Holding(TimeStampedModel):
    class Meta:
        verbose_name = '取置'
        verbose_name_plural = '取置'

    stock = models.OneToOneField(
        Stock,
        verbose_name='蔵書',
        related_name='holding',
        on_delete=models.PROTECT
    )
    user = models.ForeignKey(
        User,
        verbose_name='ユーザー',
        related_name='holdings',
        on_delete=models.CASCADE
    )
    expiration_date = models.DateField(
        '有効期限'
    )

    def __str__(self):
        return '{} : {}'.format(self.stock, self.user)

    def is_expired(self):
        return self.expiration_date < timezone.localdate()
