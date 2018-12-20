from opac.queries import QueryError, HoldingLendQuery
from opac.services import ServiceError


class HoldingLendService:
    """取置の貸出処理を行うサービス。

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
            貸出処理でエラーが発生した場合。
        """
        try:
            HoldingLendQuery(self._holding).exec()
        except QueryError as e:
            raise ServiceError(self.__class__, e)
