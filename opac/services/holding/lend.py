from django.db import Error, IntegrityError

from opac.queries import HoldingLendQuery
from opac.services import LendingAlreadyExistsError, ServiceError


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
        LendingAlreadyExistsError
            既に貸出が存在していた場合
        ServiceError
            貸出処理でエラーが発生した場合
        """
        try:
            HoldingLendQuery(self._holding).exec()
        except IntegrityError as e:
            raise LendingAlreadyExistsError(self._holding, e)
        except Error as e:
            raise ServiceError(self._holding, e)
