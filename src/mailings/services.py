from typing import Union

from src.cases.models import Case
from src.mailings.mailchimp_services import add_mailchimp_email_with_tag
from src.mailings.models import CommonMailingList, CaseMailingList


def add_email_to_common_mailchimp_list(email: str):
    """Добавляет email в общий лист рассылки """

    add_mailchimp_email_with_tag(audience_name='COMMON',
                                 email=email,
                                 tag='COMMON TAG')

    # Добавляем email в DB, т.к. мы хотим чтобы данный email сохранился не только в mailchimp
    # аудитории, но и в нашей базе данных.
    CommonMailingList.objects.get_or_create(email=email)


def add_email_to_case_mailchimp_list(email: str, case_id: Union[int, str]):
    """Добавляет email в общий лист рассылки """

    # case_id у нас может быть либо строчкой, либо целым
    case = Case.objects.get(pk=case_id)
    add_mailchimp_email_with_tag(audience_name='CASES',
                                 email=email,
                                 tag=f'Case {case.name}')

    # Добавляем email в DB, т.к. мы хотим чтобы данный email сохранился не только в mailchimp
    # аудитории, но и в нашей базе данных.
    CaseMailingList.objects.get_or_create(email=email)
