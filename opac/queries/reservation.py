from datetime import timedelta

from django.utils import timezone

from opac.models.transactions import Holding


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
        bool
            最初の予約を取置に繰り上げたかどうか
        """
        if self._reservation:
            Holding.objects.create(
                stock=self._reservation.stock,
                user=self._reservation.user,
                expiration_date=timezone.localdate() + timedelta(days=14)
            )
            self._reservation.delete()
            return True
        else:
            return False
