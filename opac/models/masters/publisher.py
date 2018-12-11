from django.db import models

from opac.models.abstracts import TimeStampedModel


class Publisher(TimeStampedModel):
    class Meta:
        verbose_name = '出版者'
        verbose_name_plural = '出版者'

    name = models.CharField(
        '名前',
        max_length=100
    )
    address = models.CharField(
        '所在地',
        max_length=100,
        blank=True,
        null=True
    )

    def __str__(self):
        return self.name
