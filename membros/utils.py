from __future__ import absolute_import, unicode_literals
from datetime import date, timedelta
from .models import Membros
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from django.conf import settings
import os

def get_aniversariantes_da_semana():
    hoje = date.today()
    inicio_semana = hoje - timedelta(days=hoje.weekday())  # Segunda-feira
    fim_semana = inicio_semana + timedelta(days=6)  # Domingo

    aniversariantes = Membros.objects.filter(
        data_nascimento__month=hoje.month,
        data_nascimento__day__range=(inicio_semana.day, fim_semana.day)
    )
    return aniversariantes

def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    
    # Importando weasyprint conforme usado no views.py
    from weasyprint import HTML
    HTML(string=html).write_pdf(result)
    
    if result:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None

# Código relacionado ao Celery foi comentado pois o módulo não está instalado
# import os
# from celery import Celery
# from celery.schedules import crontab

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')

# app = Celery('mysite')
# app.config_from_object('django.conf:settings', namespace='CELERY')
# app.autodiscover_tasks()

# app.conf.beat_schedule = {
#     'enviar-aviso-aniversariantes-sexta-feira': {
#         'task': 'membros.tasks.enviar_aviso_aniversariantes',
#         'schedule': crontab(hour=9, minute=0, day_of_week=5),  # Sexta-feira às 9:00
#     },
# }

# from .celery import app as celery_app

# __all__ = ('celery_app',)

# from celery import shared_task
# from .utils import get_aniversariantes_da_semana

# @shared_task
# def enviar_aviso_aniversariantes():
#     aniversariantes = get_aniversariantes_da_semana()
#     # Lógica para enviar o aviso (por exemplo, enviar um e-mail)
#     for membro in aniversariantes:
#         print(f"Aniversariante: {membro.nome}")