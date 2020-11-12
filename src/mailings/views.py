from django.http import JsonResponse

from .services import add_email_to_common_mailchimp_list, \
    add_email_to_case_mailchimp_list


def add_email_to_common_mailchimp_list_view(request):
    """Веб-сервис добавляющий email в общий лист рассылки в mailchimp"""

    email = request.GET.get('email')
    if not email:
        return JsonResponse({'success': False, 'message': 'Передайте email'})
    add_email_to_common_mailchimp_list(email=email)
    return JsonResponse({'success': True})


def add_email_to_case_mailchimp_list_vie(request):
    """Веб-сервис, добавляющий email в лист рассылок по конкретному делу"""

    email = request.GET.get('email')

    if not email:
        return JsonResponse({'success': False, 'message': 'Передайте email'})

    case_id = request.GET.get('case_id')
    # Проверяем, что он не пустой
    if not case_id:
        return JsonResponse({'success': False, 'message': 'Передайте case_id'})
    add_email_to_case_mailchimp_list(email=email, case_id=case_id)
    return JsonResponse({'success': True})
