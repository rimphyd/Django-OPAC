from django.db import models

from opac.models.abstracts import TimeStampedModel


class Library(TimeStampedModel):
    class Meta:
        verbose_name = '図書館'
        verbose_name_plural = '図書館'

    name = models.CharField(
        '館名',
        max_length=100,
        unique=True
    )
    address = models.CharField(
        '所在地',
        max_length=100,
        unique=True
    )

    def __str__(self):
        return self.name
