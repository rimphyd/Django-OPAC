from django.core import mail
from django.test import TestCase
from django.utils import timezone

from opac.models.masters import Stock, User
from opac.models.transactions import Holding, Reservation
from opac.services.holding import HoldingCancelService


class HoldingCancelServiceSuccessTests(TestCase):
    fixtures = ['masters_minimal']

    def test_holding_count(self):
        stock = Stock.objects.get(pk=1)
        user = User.objects.get(pk=1)
        holding = Holding.objects.create(
            stock=stock,
            user=user,
            expiration_date=timezone.localdate()
        )
        self.assertEqual(Holding.objects.count(), 1)
        HoldingCancelService(holding).exec()
        self.assertEqual(Holding.objects.count(), 0)

    def test_has_no_effect_on_unrelated_reservation(self):
        stock1 = Stock.objects.get(pk=1)
        stock2 = Stock.objects.get(pk=2)
        user = User.objects.get(pk=1)
        holding = Holding.objects.create(
            stock=stock1,
            user=user,
            expiration_date=timezone.localdate()
        )
        reservation = Reservation.objects.create(
            stock=stock2,
            user=user
        )
        self.assertEqual(Reservation.objects.count(), 1)
        HoldingCancelService(holding).exec()
        self.assertEqual(Reservation.objects.count(), 1)
        self.assertEqual(reservation, Reservation.objects.get(pk=1))

    def test_remove_first_reservation_and_create_holding(self):
        stock = Stock.objects.get(pk=1)
        user1 = User.objects.get(pk=1)
        user2 = User.objects.get(pk=2)
        user3 = User.objects.get(pk=3)
        holding = Holding.objects.create(
            stock=stock,
            user=user1,
            expiration_date=timezone.localdate()
        )
        Reservation.objects.create(
            stock=stock,
            user=user2
        )
        Reservation.objects.create(
            stock=stock,
            user=user3
        )
        self.assertEqual(Holding.objects.count(), 1)
        self.assertEqual(Reservation.objects.count(), 2)
        HoldingCancelService(holding).exec()
        self.assertEqual(Holding.objects.count(), 1)
        self.assertEqual(Reservation.objects.count(), 1)
        self.assertEqual(Holding.objects.get(pk=2).user, user2)
        self.assertEqual(Reservation.objects.get(pk=2).user, user3)

    def test_mail_to_first_reservation_user(self):
        stock = Stock.objects.get(pk=1)
        user1 = User.objects.get(pk=1)
        user2 = User.objects.get(pk=2)
        holding = Holding.objects.create(
            stock=stock,
            user=user1,
            expiration_date=timezone.localdate()
        )
        Reservation.objects.create(
            stock=stock,
            user=user2
        )
        self.assertEqual(len(mail.outbox), 0)
        HoldingCancelService(holding).exec()
        self.assertEqual(len(mail.outbox), 1)
        self.assertIs('蔵書取り置きのご連絡' in mail.outbox[0].subject, True)
        self.assertIs(user2.username in str(mail.outbox[0].body), True)
        self.assertIs(stock.book.name in str(mail.outbox[0].body), True)
