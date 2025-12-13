# finance/tasks.py
from celery import shared_task
from django.utils import timezone
from core.models import Fee

@shared_task
def check_overdue_fees():
    overdue = Fee.objects.filter(due_date__lt=timezone.now(), is_paid=False)
    for fee in overdue:
        # Pseudo-code for notification
        send_sms(fee.student.phone, "Your fee is overdue!")