from opac.queries import QueryError, RenewingCreateQuery
from opac.services.errors import ServiceError


class LendingRenewService:
    """貸出を延長するサービス。

    Parameter
    ---------
    lending
        対象の貸出
    """
    def __init__(self, lending):
        self._lending = lending

    def exec(self):
        """サービスを実行する。

        Raises
        ------
        ServiceError
            貸出の延長でエラーが発生した場合
        """
        try:
            RenewingCreateQuery(self._lending).exec()
        except QueryError as e:
            raise ServiceError(self.__class__, e)
