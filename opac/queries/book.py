from functools import reduce
from operator import or_

from django.db.models import Q

from opac.models.masters import Book


class BookSearchQuery:
    def __init__(self, words):
        self._words = words

    def query(self):
        querysets = (
            Book.objects
                .filter(
                    Q(name__icontains=word) |
                    Q(authors__name__icontains=word) |
                    Q(translators__name__icontains=word) |
                    Q(publisher__name__icontains=word))
                .distinct()
            for word in self._words
        )
        return reduce(or_, querysets).order_by('-issue_date')


class BookQuery:
    def __init__(self, book_id):
        self._book_id = book_id

    def query(self):
        return Book.objects.get(pk=self._book_id)
