from typing import Optional
from mailchimp3 import MailChimp

from django.http import JsonResponse
from django.conf import settings

from .models import CommonMailingList, CaseMailingList
from cases.models import Case
from .mailchimp_services import add_mailchimp_email_with_tag


def add_to_common_list_view(request):
    """Веб-сервис добавляющий email в общий лист рассылки в mailchimp"""
    # Получаем email
    email = request.GET.get('email')

    # Проверяем, что он не пустой
    # Логика по проверки входных данных может находится во слое вьюшки.
    # Это просто валидация данных, а не бизнес длогика
    if not email:
        return JsonResponse({'success': False, 'message': 'Передайте email'})

    add_mailchimp_email_with_tag(audience_id=settings.MAILCHIMP_COMMON_LIST_ID,
                                 email=email,
                                 tag='COMMON TAG')

    # Добавляем email в DB, т.к. мы хотим чтобы данный email сохранился не только в mailchimp
    # аудитории, но и в нашей базе данных.
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

    # Мы получаем дело из базы данных
    case = Case.objects.get(pk=case_id)
    case_tag = f'Case {case.name}'

    add_mailchimp_email_with_tag(audience_id=settings.MAILCHIMP_CASE_LIST_ID,
                                 email=email,
                                 tag=case_tag)
    # Добавляем email в DB
    CaseMailingList.objects.get_or_create(email=email, case=case)

    # Допустим у нас простинький сервис который возвращает только такой Json.
    return JsonResponse({'success': True})
