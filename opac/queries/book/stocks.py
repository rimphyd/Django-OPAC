from opac.models.masters import Stock


class BookStocksQuery:
    def __init__(self, book_id):
        self._book_id = book_id

    def exec(self):
        return (
            Stock.objects
                 .filter(book_id=self._book_id)
                 .select_related('library')
                 .select_related('lending')
                 .select_related('lending__renewing')
                 .select_related('holding')
                 .prefetch_related('reservations')
                 .order_by('library__id')
        )
