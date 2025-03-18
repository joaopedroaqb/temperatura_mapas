from django_celery_beat.models import PeriodicTask, IntervalSchedule

def setup_update_point_details():
    """
    Configura a tarefa periódica no django-celery-beat.
    """
    # Cria ou recupera o agendamento de intervalo (10 segundos)
    schedule, created = IntervalSchedule.objects.get_or_create(
        every=1,
        period=IntervalSchedule.MINUTES,
    )

    # Cria ou recupera a tarefa periódica
    PeriodicTask.objects.get_or_create(
        interval=schedule,
        name='Minha tarefa periódica',  
        task='maps.tasks.update_point_details',  
    )