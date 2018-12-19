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
        bool
            最初の予約を取置に繰り上げた場合かどうか

        Raises
        ------
        QueryError
            クエリでエラーが発生した場合
        """
        stock = self._lending.stock
        try:
            holding_created = FirstReservationToHoldingQuery(stock).exec()
            self._lending.delete()
        except Error as e:
            # TODO ログを仕込む
            raise QueryError(self._lending, e)
        else:
            return holding_created
