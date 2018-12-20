from django.test import TestCase

from opac.models.masters import Book, Publisher


class SearchViewRequestDispatchTests(TestCase):
    def test_no_params(self):
        response = self.client.get('/search/')
        self.assertContains(response, '検索語を入力してください。')

    def test_empty_words(self):
        response = self.client.get('/search/?words=')
        self.assertContains(response, '検索語を入力してください。')

    def test_space_words(self):
        response = self.client.get('/search/?words= ')
        self.assertContains(response, '検索語を入力してください。')


class SearchViewRenderToResponseTests(TestCase):
    def test_no_books(self):
        response = self.client.get('/search/?words=hoge')
        self.assertContains(response, '該当する書籍が見つかりませんでした。')

    def test_books(self):
        publisher = Publisher.objects.create(name='pub')
        Book.objects.create(name='hoge', publisher=publisher)
        response = self.client.get('/search/?words=hoge')
        self.assertNotContains(response, '該当する書籍が見つかりませんでした。')
