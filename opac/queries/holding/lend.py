from datetime import timedelta

from django.db import Error, IntegrityError, transaction
from django.utils import timezone

from opac.models.transactions import Lending
from opac.queries.errors import AlreadyExistsError, QueryError


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
        AlreadyExistsError
            既に貸出が存在していた場合
        QueryError
            その他のエラーが発生した場合
        """
        try:
            Lending.objects.create(
                stock=self._holding.stock,
                user=self._holding.user,
                due_date=timezone.localdate() + timedelta(days=14)
            )
            self._holding.delete()
        except IntegrityError as e:
            raise AlreadyExistsError(self._holding, e)
        except Error as e:
            raise QueryError(self._holding, e)
