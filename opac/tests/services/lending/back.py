from django.core import mail
from django.test import TestCase
from django.utils import timezone

from opac.models.masters import Stock, User
from opac.models.transactions import Holding, Lending, Reservation
from opac.services.lending import LendingBackService


class LendingBackServiceSuccessTests(TestCase):
    fixtures = ['initial_data']

    def test_lending_count(self):
        stock = Stock.objects.get(pk=1)
        user = User.objects.get(pk=1)
        lending = Lending.objects.create(
            stock=stock,
            user=user,
            due_date=timezone.localdate()
        )
        self.assertEqual(Lending.objects.count(), 1)
        LendingBackService(lending).exec()
        self.assertEqual(Lending.objects.count(), 0)

    def test_has_no_effect_on_unrelated_reservation(self):
        stock1 = Stock.objects.get(pk=1)
        stock2 = Stock.objects.get(pk=2)
        user = User.objects.get(pk=1)
        lending = Lending.objects.create(
            stock=stock1,
            user=user,
            due_date=timezone.localdate()
        )
        reservation = Reservation.objects.create(
            stock=stock2,
            user=user
        )
        self.assertEqual(Reservation.objects.count(), 1)
        LendingBackService(lending).exec()
        self.assertEqual(Reservation.objects.count(), 1)
        self.assertEqual(reservation, Reservation.objects.get(pk=1))

    def test_remove_first_reservation_and_create_holding(self):
        stock = Stock.objects.get(pk=1)
        user1 = User.objects.get(pk=1)
        user2 = User.objects.get(pk=2)
        user3 = User.objects.get(pk=3)
        lending = Lending.objects.create(
            stock=stock,
            user=user1,
            due_date=timezone.localdate()
        )
        Reservation.objects.create(
            stock=stock,
            user=user2
        )
        Reservation.objects.create(
            stock=stock,
            user=user3
        )
        self.assertEqual(Lending.objects.count(), 1)
        self.assertEqual(Reservation.objects.count(), 2)
        LendingBackService(lending).exec()
        self.assertEqual(Lending.objects.count(), 0)
        self.assertEqual(Holding.objects.count(), 1)
        self.assertEqual(Reservation.objects.count(), 1)
        self.assertEqual(Holding.objects.get(pk=1).user, user2)
        self.assertEqual(Reservation.objects.get(pk=2).user, user3)

    def test_mail_to_first_reservation_user(self):
        stock = Stock.objects.get(pk=1)
        user1 = User.objects.get(pk=1)
        user2 = User.objects.get(pk=2)
        lending = Lending.objects.create(
            stock=stock,
            user=user1,
            due_date=timezone.localdate()
        )
        Reservation.objects.create(
            stock=stock,
            user=user2
        )
        self.assertEqual(len(mail.outbox), 0)
        LendingBackService(lending).exec()
        self.assertEqual(len(mail.outbox), 1)
        self.assertIs('蔵書取り置きのご連絡' in mail.outbox[0].subject, True)
        self.assertIs(user2.username in str(mail.outbox[0].body), True)
        self.assertIs(stock.book.name in str(mail.outbox[0].body), True)
