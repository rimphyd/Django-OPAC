from django.views.generic import DetailView

from opac.models.masters import Book


class BookDetailView(DetailView):
    model = Book

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['stocks'] = context['book'].ordered_stocks()
        return context
