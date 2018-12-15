from django.db import models
from django.utils import timezone

from opac.models.abstracts import TimeStampedModel
from opac.models.transactions.lending import Lending


class Renewing(TimeStampedModel):
    class Meta:
        verbose_name = '延長'
        verbose_name_plural = '延長'

    lending = models.OneToOneField(
        Lending,
        verbose_name='貸出',
        related_name='renewing',
        on_delete=models.CASCADE
    )
    due_date = models.DateField(
        '延長期限'
    )

    def __str__(self):
        return str(self.lending)

    def is_overdue(self):
        return self.due_date < timezone.localdate()
