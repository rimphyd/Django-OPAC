from django.urls import path

from . import views


app_name = 'opac'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('search/', views.SearchView.as_view(), name='search'),
    path('book/<int:pk>/',
         views.BookDetailView.as_view(), name='book_detail'),
]
