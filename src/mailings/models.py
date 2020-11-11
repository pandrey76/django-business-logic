from django.db import models

# Создаём две отдельные модели


class CommonMailingList(models.Model):
    """Рассылка на общие материалы с сайта"""
    email = models.EmailField('Email подписчика')

    class Meta:
        # Имя таблички в базе данных
        db_table = "common_mailing_list"


class CaseMailingList(models.Model):
    """Рассылка на материалы конкретного дела"""
    email = models.EmailField('Email подписчика')
    case = models.ForeignKey(to='cases.Case', verbose_name='Дело', on_delete=models.CASCADE)

    class Meta:
        db_table = 'case_mailing_list'
