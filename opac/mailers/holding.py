from smtplib import SMTPException

from django.core.mail import send_mail

from opac.mailers import MailerError


class HoldingCreatedMailer:
    """取置連絡をするメーラー。

    Parameters
    ----------
    holding
        対象の取置
    """
    def __init__(self, holding):
        self._name = holding.user.username
        self._book = holding.stock.book
        self._expiration_date = holding.expiration_date
        self._email = holding.user.email

    def exec(self):
        """メールを送信する。

        Raises
        ------
        MailerError
            メール送信でエラーが発生した場合
        """
        try:
            send_mail(
                '蔵書取り置きのご連絡 ○○○図書館',
                '{} さんが予約されていた {} を取り置きしました。\n取置期限は{}です。'.format(
                    self._name,
                    self._book,
                    self._expiration_date
                ),
                'from@django-opac.com',
                [self._email],
                fail_silently=False,
            )
        except SMTPException as e:
            raise MailerError(self.__class__, e)
