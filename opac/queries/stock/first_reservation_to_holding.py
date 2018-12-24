from datetime import timedelta

from django.db import Error, IntegrityError
from django.utils import timezone

from opac.models.transactions import Holding
from opac.queries.errors import AlreadyExistsError, QueryError


class FirstReservationToHoldingQuery:
    """最初の予約を取置に繰り上げるクエリ。

    Parameters
    ----------
    stock
        対象の蔵書
    """
    def __init__(self, stock):
        self._reservation = stock.reservations.order_by('created_at').first()

    def exec(self):
        """クエリを実行する。

        Detail
        ------
        予約が存在する場合
            1. 最初の予約に対応する取置を作成する
            2. 最初の予約を削除する
        予約が存在しない場合
            1. 何もしない

        Returns
        -------
        取置を作成した場合
            作成した取置

        取置を作成しなかった場合
            None

        Raises
        ------
        AlreadyExistsError
            最初の予約に対応する取置が既に存在していた場合
        QueryError
            その他のエラーが発生した場合
        """
        if not self._reservation:
            return None

        try:
            self._reservation.delete()
            return Holding.objects.create(
                stock=self._reservation.stock,
                user=self._reservation.user,
                expiration_date=timezone.localdate() + timedelta(days=14)
            )
        except IntegrityError as e:
            raise AlreadyExistsError(self._reservation, e)
        except Error as e:
            raise QueryError(self._reservation, e)
