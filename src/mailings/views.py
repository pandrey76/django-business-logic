from mailchimp3 import MailChimp

from django.http import JsonResponse
from django.conf import settings

from .models import CommonMailingList


def add_to_common_list_view(request):
    """Веб-сервис добавляющий email в общий лист рассылки в mailchimp"""
    # Получаем email
    email = request.GET.get('email')

    # Проверяем, что он не пустой
    if not email:
        return JsonResponse({'success': False, 'message': 'Передайте email'})

    # Создаём mailchimp клиент
    mailchimp_client = MailChimp(
        mc_api=settings.MAILCHIMP_API_KEY,
        mc_user=settings.MAILCHIMP_USERNAME)
    # Далее нам надо добавить наш email в аудиторию common (аудиторию общих рассылок) и
    # и навесить на него какой-нибудь общий тэг, допустим тотже Common (какой-то общий тэг)

    # Данный запрос добавит наш email в аудиторию Common mailchimp
    # Первый параметр - это итдентификатор нашей аудитории
    mailchimp_client.lists.members.create(settings.MAILCHIMP_COMMON_LIST_ID, {
        'email_address': email,
        'status': 'subscribed',
    })
    # Hash нашего клиента в mailchimp (Идентификатор нашего email в аудитории mailchimp)
    subscriber_hash = mailchimp_client \
        .search_members \
        .get(query=email, fields='exact_matches.members.id') \
        .get('exact_matches') \
        .get('members')[0].get('id')

    # Добавляем tag нашему клиенту (email в mailchimp)
    mailchimp_client.lists.members.tags.update(
        list_id=settings.MAILCHIMP_COMMON_LIST_ID,
        subscriber_hash=subscriber_hash,
        data={'tag': [{'name': 'COMMON TAG', 'status': 'active'}]})

    # Добавляем email в DB
    CommonMailingList.objects.get_or_create(email=email)

    # Допустим у нас простинький сервис который возвращает только такой Json.
    return JsonResponse({'success': True})
