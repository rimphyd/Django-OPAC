from django.db import transaction

from opac.queries.stock import FirstReservationToHoldingQuery


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
        stock = self._holding.stock
        self._holding.delete()
        return FirstReservationToHoldingQuery(stock).exec()
