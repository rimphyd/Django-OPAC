from opac.queries import QueryError, HoldingCancelQuery
from opac.services import ServiceError


class HoldingCancelService:
    """取置の取り消しを行うサービス。

    Parameters
    ----------
    holding
        対象の取置
    """
    def __init__(self, holding):
        self._holding = holding

    def exec(self):
        """サービスを実行する。

        Raises
        ------
        ServiceError
            取り消し処理でエラーが発生した場合。
        """
        try:
            holding_created = HoldingCancelQuery(self._holding).exec()
            if holding_created:
                # TODO メールを送る
                pass
        except QueryError as e:
            raise ServiceError(self.__class__, e)
