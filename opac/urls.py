from django.urls import path

from . import views


app_name = 'opac'
urlpatterns = [
    path('', views.index, name='index'),
]
