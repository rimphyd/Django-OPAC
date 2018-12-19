from datetime import timedelta

from django.db import Error, transaction
from django.utils import timezone

from opac.models.transactions import Lending
from opac.queries.errors import QueryError
from opac.queries.reservation import FirstReservationToHoldingQuery


class HoldingLendQuery:
    """取置の貸出処理を行うクエリ。アトミックです。

    Parameters
    ----------
    holding
        対象の取置
    """
    def __init__(self, holding):
        self._holding = holding

    @transaction.atomic
    def exec(self):
        """クエリを実行する。

        Detail
        ------
        1. 取置に対応する貸出を作成する
        2. 取置を削除する

        Raises
        ------
        QueryError
            クエリでエラーが発生した場合
        """
        try:
            Lending.objects.create(
                stock=self._holding.stock,
                user=self._holding.user,
                due_date=timezone.localdate() + timedelta(days=14)
            )
            self._holding.delete()
        except Error as e:
            raise QueryError(self._holding, e)


class HoldingCancelQuery:
    """取置の取り消し処理を行うクエリ。アトミックです。

    Parameters
    ----------
    holding
        対象の取置
    """
    def __init__(self, holding):
        self._holding = holding

    @transaction.atomic
    def exec(self):
        """クエリを実行する。

        Detail
        ------
        蔵書に予約が存在する場合
            1. 取置を削除する
            2. 最初の予約に対応する取置を作成する
            3. 最初の予約を削除する

        蔵書に予約が存在しない場合
            1. 取置を削除する

        Returns
        -------
        bool
            最初の予約を取置に繰り上げたかどうか

        Raises
        ------
        QueryError
            クエリでエラーが発生した場合
        """
        stock = self._holding.stock
        try:
            self._holding.delete()
            holding_created = FirstReservationToHoldingQuery(stock).exec()
        except Error as e:
            # TODO ログを仕込む
            raise QueryError(self._holding, e)
        else:
            return holding_created
