from django.urls import path

from . import views


app_name = 'opac'
urlpatterns = [
    path('search/', views.SearchView.as_view(), name='search'),
    path('book/', views.BookListView.as_view(), name='book_list'),
]
