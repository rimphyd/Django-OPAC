from datetime import timedelta

from django.db import Error
from django.utils import timezone

from opac.models.transactions import Renewing
from opac.queries import QueryError


class RenewingCreateQuery:
    """貸出に対応する延長を作成するクエリ。

    Parameters
    ----------
    lending
        対象の貸出
    """
    def __init__(self, lending):
        self._lending = lending

    def exec(self):
        """クエリを実行する。

        Raises
        ------
        QueryError
            クエリでエラーが発生した場合
        """
        try:
            Renewing.objects.create(
                lending=self._lending,
                due_date=timezone.localdate() + timedelta(days=14)
            )
        except Error as e:
            raise QueryError(self.__class__, self._lending, e)
