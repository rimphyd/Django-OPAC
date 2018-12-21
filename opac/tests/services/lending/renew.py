from django.test import TestCase, TransactionTestCase
from django.utils import timezone

from opac.models.masters import Stock, User
from opac.services import LendingRenewService
from opac.services.errors import \
    RenewingAlreadyExistsError, ReservationExistsError
from opac.models.transactions import Lending, Renewing, Reservation


class LendingRenewServiceSuccessTests(TestCase):
    fixtures = ['initial_data']

    def test_create_renewing(self):
        lending = Lending.objects.create(
            stock=Stock.objects.get(pk=1),
            user=User.objects.get(pk=1),
            due_date=timezone.localdate()
        )
        self.assertEqual(Lending.objects.count(), 1)
        self.assertEqual(Renewing.objects.count(), 0)
        LendingRenewService(lending).exec()
        self.assertEqual(Lending.objects.count(), 1)
        self.assertEqual(Renewing.objects.count(), 1)
        self.assertEqual(Renewing.objects.get(pk=1).lending, lending)


class LendingRenewServiceFailureTests(TransactionTestCase):
    fixtures = ['initial_data']

    def test_renewing_already_exists(self):
        lending = Lending.objects.create(
            stock=Stock.objects.get(pk=1),
            user=User.objects.get(pk=1),
            due_date=timezone.localdate()
        )
        Renewing.objects.create(
            lending=lending,
            due_date=timezone.localdate()
        )
        self.assertEqual(Lending.objects.count(), 1)
        self.assertEqual(Renewing.objects.count(), 1)
        service = LendingRenewService(lending)
        self.assertRaises(RenewingAlreadyExistsError, service.exec)
        self.assertEqual(Renewing.objects.count(), 1)

    def test_reservation_exists(self):
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
        self.assertEqual(Lending.objects.count(), 1)
        self.assertEqual(Renewing.objects.count(), 0)
        self.assertEqual(Reservation.objects.count(), 1)
        service = LendingRenewService(lending)
        self.assertRaises(ReservationExistsError, service.exec)
        self.assertEqual(Renewing.objects.count(), 0)
