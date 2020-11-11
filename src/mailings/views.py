from django.http import JsonResponse


def add_to_common_list_view(request):
    """Веб-сервис добавляющий email общий лист рассылки"""
    # Допустим у нас простинький сервис который возвращает только такой Json.
    return JsonResponse({'success':True})