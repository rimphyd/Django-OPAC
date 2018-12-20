from opac.queries import LendingBackQuery, QueryError
from opac.services.errors import ServiceError


class LendingBackService:
    """貸出の返却処理と取置ユーザーへのメール送信を行うサービス。

    Parameters
    ----------
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
            返却処理やメール送信でエラーが発生した場合。
        """
        try:
            holding_created = LendingBackQuery(self._lending).exec()
            if holding_created:
                # TODO メールを送る
                pass
        except QueryError as e:
            raise ServiceError(self.__class__, e)
