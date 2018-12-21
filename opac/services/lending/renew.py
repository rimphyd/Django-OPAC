from django.db import Error, IntegrityError

from opac.queries import RenewingCreateQuery
from opac.services.errors import \
    RenewingAlreadyExistsError, ReservationExistsError, ServiceError


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
        RenewingAlreadyExistsError
            既に延長されている場合
        ReservationExistsError
            予約されている場合
        ServiceError
            貸出の延長でエラーが発生した場合
        """
        if self._lending.stock.is_reserved():
            raise ReservationExistsError(self._lending)
        try:
            RenewingCreateQuery(self._lending).exec()
        except IntegrityError as e:
            raise RenewingAlreadyExistsError(self._lending, e)
        except Error as e:
            raise ServiceError(self._lending, e)
