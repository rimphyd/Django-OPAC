from django.views.generic import DetailView

from opac.models.masters import Book
from opac.queries import BookStocksQuery


class BookDetailView(DetailView):
    model = Book

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book_id = self.kwargs['pk']
        context['stocks'] = BookStocksQuery(book_id).exec()
        return context
