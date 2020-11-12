from typing import Optional
from mailchimp3 import MailChimp

from django.http import JsonResponse
from django.conf import settings

from .models import CommonMailingList, CaseMailingList
from cases.models import Case


def add_to_common_list_view(request):
    """Веб-сервис добавляющий email в общий лист рассылки в mailchimp"""
    # Получаем email
    email = request.GET.get('email')

    # Проверяем, что он не пустой
    if not email:
        return JsonResponse({'success': False, 'message': 'Передайте email'})

    mailchimp_client = _get_mailchimp_client()

    # Далее нам надо добавить наш email в аудиторию common (аудиторию общих рассылок) и
    # и навесить на него какой-нибудь общий тэг, допустим тотже Common (какой-то общий тэг)

    # Данный запрос добавит наш email в аудиторию Common mailchimp
    # Первый параметр - это итдентификатор нашей аудитории
    _add_email_to_mailchimp_audience(audience_id=settings.MAILCHIMP_COMMON_LIST_ID, email=email)

    # Hash нашего клиента в mailchimp (Идентификатор нашего email в аудитории mailchimp)
    subscriber_hash = _get_mailchimp_subscribed_hash(email=email)

    # Добавляем tag нашему клиенту (email в mailchimp)
    mailchimp_client.lists.members.tags.update(
        list_id=settings.MAILCHIMP_COMMON_LIST_ID,
        subscriber_hash=subscriber_hash,
        data={'tag': [{'name': 'COMMON TAG', 'status': 'active'}]})

    # Добавляем email в DB
    CommonMailingList.objects.get_or_create(email=email)

    # Допустим у нас простинький сервис который возвращает только такой Json.
    return JsonResponse({'success': True})


def add_to_case_list_view(request):
    """Веб-сервис, добавляющий email в лист рассылок по конкретному делу"""

    email = request.GET.get('email')

    if not email:
        return JsonResponse({'success': False, 'message': 'Передайте email'})

    case_id = request.GET.get('case_id')
    # Проверяем, что он не пустой
    if not case_id:
        return JsonResponse({'success': False, 'message': 'Передайте case_id'})

    mailchimp_client = _get_mailchimp_client()

    # Данный запрос добавит наш email в аудиторию Common mailchimp
    # Первый параметр - это итдентификатор нашей аудитории
    _add_email_to_mailchimp_audience(settings.MAILCHIMP_CASE_LIST_ID, email)

    # Hash нашего клиента в mailchimp (Идентификатор нашего email в аудитории mailchimp)
    subscriber_hash = _get_mailchimp_subscribed_hash(email=email)

    # Мы получаем дело из базы данных
    case = Case.objects.get(pk=case_id)
    case_tag = f'Case {case.name}'

    # Добавляем tag нашему клиенту (email в mailchimp)
    mailchimp_client.lists.members.tags.update(
        list_id=settings.MAILCHIMP_CASE_CASE_ID,
        subscriber_hash=subscriber_hash,
        data={'tag': [{'name': case_tag, 'status': 'active'}]})

    # Добавляем email в DB
    CaseMailingList.objects.get_or_create(email=email, case=case)

    # Допустим у нас простинький сервис который возвращает только такой Json.
    return JsonResponse({'success': True})


def _get_mailchimp_client() -> MailChimp:
    """возвращает клиент API для работы Mailchimp"""
    return MailChimp(
        mc_api=settings.MAILCHIMP_API_KEY,
        mc_user=settings.MAILCHIMP_USERNAME)


def _add_email_to_mailchimp_audience(audience_id: str, email: str) -> None:
    """Добавляет email в mailchimp аудиторию с идентификатором audience_id"""
    _get_mailchimp_client().lists.members.create(audience_id, {
        'email_address': email,
        'status': 'subscribed',
    })


# def _get_mailchimp_subscribed_hash(email: str) -> Union[str, None]:
def _get_mailchimp_subscribed_hash(email: str) -> Optional[str]:
    """Возвращает идентификатор email в Mailchimp или None,
     если email там не найден """
    members = _get_mailchimp_client()  \
        .search_members \
        .get(query=email, fields='exact_matches.members.id') \
        .get('exact_matches') \
        .get('members')
    if not members:
        return None
    return members[0].get('id')

