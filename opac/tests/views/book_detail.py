from datetime import timedelta

from django.test import TestCase
from django.utils import dateformat, timezone

from opac.models.masters import Stock, User
from opac.models.transactions import Holding, Lending, Renewing, Reservation


class BookDetailViewNotFoundTest(TestCase):
    def test_book_not_found(self):
        response = self.client.get('/book/1/')
        self.assertEqual(response.status_code, 404)


class BookDetailViewStockListTest(TestCase):
    fixtures = ['masters_minimal']

    def test_all_lendable(self):
        response = self.client.get('/book/1/')
        self.assertContains(response, '貸出可能')
        self.assertNotContains(response, '取置中')
        self.assertNotContains(response, '貸出中')
        self.assertNotContains(response, '予約')

    def test_holding(self):
        stock = Stock.objects.filter(book__id=1).first()
        user = User.objects.get(pk=1)
        expiration_date = timezone.localdate()
        Holding.objects.create(
            stock=stock,
            user=user,
            expiration_date=expiration_date
        )
        display_date = dateformat.format(expiration_date, 'Y年n月d日')
        response = self.client.get('/book/1/')
        self.assertContains(response, '取置中')
        self.assertContains(response, f'[{display_date}取置期限]')
        self.assertNotContains(response, '貸出中')
        self.assertNotContains(response, '予約')

    def test_lending(self):
        stock = Stock.objects.filter(book__id=1).first()
        user = User.objects.get(pk=1)
        due_date = timezone.localdate()
        Lending.objects.create(
            stock=stock,
            user=user,
            due_date=due_date
        )
        display_date = dateformat.format(due_date, 'Y年n月j日')
        response = self.client.get('/book/1/')
        self.assertNotContains(response, '取置中')
        self.assertContains(response, '貸出中')
        self.assertContains(response, f'[{display_date}返却期限]')
        self.assertNotContains(response, '予約')

    def test_renewing(self):
        stock = Stock.objects.filter(book__id=1).first()
        user = User.objects.get(pk=1)
        due_date = timezone.localdate()
        lending = Lending.objects.create(
            stock=stock,
            user=user,
            due_date=due_date
        )
        renewing_due_date = due_date + timedelta(days=14)
        Renewing.objects.create(
            lending=lending,
            due_date=renewing_due_date
        )
        display_date = dateformat.format(renewing_due_date, 'Y年n月j日')
        response = self.client.get('/book/1/')
        self.assertNotContains(response, '取置中')
        self.assertContains(response, '貸出中')
        self.assertContains(response, f'[{display_date}返却期限]')
        self.assertNotContains(response, '予約')

    def test_reservation(self):
        stock = Stock.objects.filter(book__id=1).first()
        user = User.objects.get(pk=1)
        due_date = timezone.localdate()
        Lending.objects.create(
            stock=stock,
            user=user,
            due_date=due_date
        )
        display_date = dateformat.format(due_date, 'Y年n月j日')
        Reservation.objects.create(
            stock=stock,
            user=User.objects.get(pk=2)
        )
        Reservation.objects.create(
            stock=stock,
            user=User.objects.get(pk=3)
        )
        response = self.client.get('/book/1/')
        self.assertNotContains(response, '取置中')
        self.assertContains(response, '貸出中')
        self.assertContains(response, f'[{display_date}返却期限]')
        self.assertContains(response, '予約2人')


class BookDetailViewBookDetailTest(TestCase):
    fixtures = ['masters_minimal']

    def test_book_detail(self):
        response = self.client.get('/book/2/')
        self.assertContains(response, 'プログラミングHaskell')
        self.assertContains(response, 'Graham Hutton')
        self.assertContains(response, '山本和彦')
        self.assertContains(response, 'オーム社')
        self.assertContains(response, 'A5')
        self.assertContains(response, '232')
        self.assertContains(response, '9784274067815')
