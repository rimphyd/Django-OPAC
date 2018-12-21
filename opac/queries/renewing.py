from datetime import timedelta

from django.utils import timezone

from opac.models.transactions import Renewing


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
        IntegrityError
            既に延長が存在する場合
        Error
            その他のエラーが発生した場合
        """
        Renewing.objects.create(
            lending=self._lending,
            due_date=timezone.localdate() + timedelta(days=14)
        )
