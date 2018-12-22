from django.test import TestCase
from django.utils import timezone

from opac.models.masters import Stock, User
from opac.models.transactions import Holding, Lending, Reservation
from opac.services.errors import LendingAlreadyExistsError
from opac.services.holding import HoldingLendService


class HoldingLendServiceSuccessTests(TestCase):
    fixtures = ['masters_minimal']

    def test_holding_and_lending_counts(self):
        stock = Stock.objects.get(pk=1)
        user = User.objects.get(pk=1)
        holding = Holding.objects.create(
            stock=stock,
            user=user,
            expiration_date=timezone.localdate()
        )
        self.assertEqual(Holding.objects.count(), 1)
        self.assertEqual(Lending.objects.count(), 0)
        HoldingLendService(holding).exec()
        self.assertEqual(Holding.objects.count(), 0)
        self.assertEqual(Lending.objects.count(), 1)
        lending = Lending.objects.get(pk=1)
        self.assertEqual(stock, lending.stock)
        self.assertEqual(user, lending.user)

    def test_has_no_effect_on_reservation(self):
        stock = Stock.objects.get(pk=1)
        user1 = User.objects.get(pk=1)
        user2 = User.objects.get(pk=2)
        holding = Holding.objects.create(
            stock=stock,
            user=user1,
            expiration_date=timezone.localdate()
        )
        reservation = Reservation.objects.create(
            stock=stock,
            user=user2
        )
        self.assertEqual(Holding.objects.count(), 1)
        self.assertEqual(Lending.objects.count(), 0)
        self.assertEqual(Reservation.objects.count(), 1)
        HoldingLendService(holding).exec()
        self.assertEqual(Holding.objects.count(), 0)
        self.assertEqual(Lending.objects.count(), 1)
        self.assertEqual(Reservation.objects.count(), 1)
        lending = Lending.objects.get(pk=1)
        self.assertEqual(stock, lending.stock)
        self.assertEqual(user1, lending.user)
        self.assertEqual(reservation, Reservation.objects.get(pk=1))


class HoldingLendServiceFailureTests(TestCase):
    fixtures = ['masters_minimal']

    def test_lending_already_exists(self):
        stock = Stock.objects.get(pk=1)
        user1 = User.objects.get(pk=1)
        user2 = User.objects.get(pk=2)
        holding = Holding.objects.create(
            stock=stock,
            user=user1,
            expiration_date=timezone.localdate()
        )
        Lending.objects.create(
            stock=stock,
            user=user2,
            due_date=timezone.localdate()
        )
        service = HoldingLendService(holding)
        self.assertRaises(LendingAlreadyExistsError, service.exec)
