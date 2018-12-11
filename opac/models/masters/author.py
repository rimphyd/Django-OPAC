from django.db import models

from opac.models.abstracts import TimeStampedModel
from opac.models.masters.book import Book


class Author(TimeStampedModel):
    class Meta:
        verbose_name = '著者'
        verbose_name_plural = '著者'

    name = models.CharField(
        '氏名',
        max_length=100
    )
    books = models.ManyToManyField(
        Book,
        verbose_name='著書リスト',
        related_name='authors'
    )

    def __str__(self):
        return self.name
