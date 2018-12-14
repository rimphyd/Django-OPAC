from django.views.generic import ListView

from opac.models.masters import Book, Stock


class StockListView(ListView):
    context_object_name = 'stocks'

    def get_queryset(self):
        book_id = self.kwargs['book_id']
        return Stock.ordered_stocks(book_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book_id = self.kwargs['book_id']
        context['book'] = Book.objects.get(pk=book_id)
        return context
