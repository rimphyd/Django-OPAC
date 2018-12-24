from datetime import timedelta

from django.db import Error, IntegrityError
from django.utils import timezone

from opac.models.transactions import Renewing
from opac.queries.errors import AlreadyExistsError, QueryError


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
        AlreadyExistsError
            既に延長が存在する場合
        QueryError
            その他のエラーが発生した場合
        """
        try:
            Renewing.objects.create(
                lending=self._lending,
                due_date=timezone.localdate() + timedelta(days=14)
            )
        except IntegrityError as e:
            raise AlreadyExistsError(self._lending, e)
        except Error as e:
            raise QueryError(self._lending, e)
