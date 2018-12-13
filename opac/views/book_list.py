from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import ListView

from opac.models.masters import Book


class BookListView(ListView):
    context_object_name = 'books'
    paginate_by = 20

    def search_words_not_found(self, request):
        messsage = '検索語を入力してください。'
        messages.error(request, messsage, extra_tags='danger')
        return HttpResponseRedirect(reverse('opac:search'))

    def books_not_found(self, request):
        messsage = '該当する書籍が見つかりませんでした。'
        messages.warning(request, messsage)
        return HttpResponseRedirect(reverse('opac:search'))

    def dispatch(self, request, *args, **kwargs):
        if 'words' not in request.GET:
            return self.search_words_not_found(request)
        if request.GET['words'].split() == []:
            return self.search_words_not_found(request)
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        words = self.request.GET['words'].split()
        return Book.search(words)

    def render_to_response(self, context, **response_kwargs):
        if not context['books']:
            return self.books_not_found(self.request)
        return super().render_to_response(context, **response_kwargs)
