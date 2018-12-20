from django.contrib import messages
from django.shortcuts import render
from django.views.generic import ListView

from opac.queries import BookSearchQuery


class SearchView(ListView):
    context_object_name = 'books'
    paginate_by = 20

    def render_index(self, request):
        return render(request, 'opac/index.html')

    def render_no_search_words(self, request):
        messsage = '検索語を入力してください。'
        messages.error(request, messsage, extra_tags='danger')
        return self.render_index(request)

    def render_no_books(self, request):
        messsage = '該当する書籍が見つかりませんでした。'
        messages.warning(request, messsage)
        return self.render_index(request)

    def dispatch(self, request, *args, **kwargs):
        if 'words' not in request.GET:
            return self.render_index(request)
        if request.GET['words'].split() == []:
            return self.render_no_search_words(request)
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        words = self.request.GET['words'].split()
        return BookSearchQuery(words).exec()

    def render_to_response(self, context, **response_kwargs):
        if not self.object_list:
            return self.render_no_books(self.request)
        return super().render_to_response(context, **response_kwargs)
