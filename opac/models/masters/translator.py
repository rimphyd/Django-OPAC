from django.db import models

from opac.models.abstracts import TimeStampedModel
from opac.models.masters.book import Book


class Translator(TimeStampedModel):
    class Meta:
        verbose_name = '訳者'
        verbose_name_plural = '訳者'

    name = models.CharField(
        '氏名',
        max_length=100
    )
    books = models.ManyToManyField(
        Book,
        verbose_name='訳書リスト',
        related_name='translators'
    )

    def __str__(self):
        return self.name
