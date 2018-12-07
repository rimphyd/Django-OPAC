from django.http import Http404, HttpResponse
from django.views.generic.base import TemplateView


class SearchView(TemplateView):
    template_name = 'opac/search.html'


def book_list(request):
    try:
        return HttpResponse(request.GET['text'])
    except KeyError:
        raise Http404
