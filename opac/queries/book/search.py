from functools import reduce
from operator import or_

from django.db.models import Q

from opac.models.masters import Book


class BookSearchQuery:
    def __init__(self, words):
        self._words = words

    def exec(self):
        querysets = (
            Book.objects
                .select_related('publisher')
                .prefetch_related('authors')
                .prefetch_related('translators')
                .filter(
                    Q(name__icontains=word) |
                    Q(authors__name__icontains=word) |
                    Q(translators__name__icontains=word) |
                    Q(publisher__name__icontains=word))
                .distinct()
            for word in self._words
        )
        return reduce(or_, querysets).order_by('-issue_date')
