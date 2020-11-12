from django.shortcuts import render

from src.mailings.mailchimp_services import add_mailchimp_email_with_tag


# Вебхук, который пришёл о факте успешной оплаты из какой-нибудь платёжной системы
# нащей системы Донатов.
def webhook(request):
    """Обработчик Вебхук от платёжной системы"""

    # Здесь нам надо подтвердить, что наш платёж правильный, сохранить эту всю историю в базу данных и
    # помимо всего прочего нам нуно отправить этот email в некую аудиторию mailchimp.
    add_mailchimp_email_with_tag(email=request.POST.get('email'),
                                 audience_name='DONATES',
                                 tag='DONATE')
