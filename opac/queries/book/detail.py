from opac.models.masters import Book


class BookDetailQuery:
    def __init__(self, book_id):
        self._book_id = book_id

    def exec(self):
        queryset = (
            Book.objects
                .filter(pk=self._book_id)
                .select_related('publisher')
                .prefetch_related('authors')
                .prefetch_related('translators')
        )
        return queryset
