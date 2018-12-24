from django.views.generic import DetailView

from opac.queries import BookDetailQuery, BookStocksQuery


class BookDetailView(DetailView):
    def get_queryset(self):
        return BookDetailQuery(self.kwargs['pk']).exec()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book_id = self.kwargs['pk']
        context['stocks'] = BookStocksQuery(book_id).exec()
        return context
