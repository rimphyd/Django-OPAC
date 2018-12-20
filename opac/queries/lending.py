from django.db import Error, transaction

from opac.queries import QueryError
from opac.queries.reservation import FirstReservationToHoldingQuery


class LendingBackQuery:
    """貸出の返却処理を行うクエリ。アトミックです。

    Parameters
    ----------
    lending
        対象の貸出
    """
    def __init__(self, lending):
        self._lending = lending

    @transaction.atomic
    def exec(self):
        """クエリを実行する。

        Detail
        ------
        蔵書に予約が存在する場合
            1. 最初の予約に対応する取置を作成する
            2. 最初の予約を削除する
            3. 貸出を削除する

        蔵書に予約が存在しない場合
            1. 貸出を削除する

        Returns
        -------
        取置を作成した場合
            作成した取置

        取置を作成しなかった場合
            None

        Raises
        ------
        QueryError
            クエリでエラーが発生した場合
        """
        stock = self._lending.stock
        try:
            created_holding = FirstReservationToHoldingQuery(stock).exec()
            self._lending.delete()
        except Error as e:
            raise QueryError(self.__class__, self._lending, e)
        else:
            return created_holding
