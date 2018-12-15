from django.db import models

from opac.models.abstracts import TimeStampedModel
from opac.models.masters.book import Book
from opac.models.masters.library import Library


class Stock(TimeStampedModel):
    class Meta:
        verbose_name = '蔵書'
        verbose_name_plural = '蔵書'

    book = models.ForeignKey(
        Book,
        verbose_name='書籍',
        related_name='stocks',
        on_delete=models.PROTECT
    )
    library = models.ForeignKey(
        Library,
        verbose_name='配架先',
        related_name='stocks',
        on_delete=models.PROTECT
    )

    def __str__(self):
        return '蔵書番号{} : {}'.format(self.id, self.book.name)

    def is_lendable(self):
        return not self.is_lent() \
           and not self.is_held()

    def is_holdable(self):
        return self.is_lendable()

    def is_reservable(self):
        return not self.is_lendable()

    def is_lent(self):
        return hasattr(self, 'lending')

    def is_held(self):
        return hasattr(self, 'holding')

    def is_reserved(self):
        return self.reservations.exists()
