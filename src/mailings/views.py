from django.http import JsonResponse


def add_to_common_list_view(request):
    """Веб-сервис добавляющий email общий лист рассылки"""
    email = request.GET.get('email')

    if not email:
        return JsonResponse({'success': False, 'message': 'Передайте email'})

    # Допустим у нас простинький сервис который возвращает только такой Json.
    return JsonResponse({'success': True})
