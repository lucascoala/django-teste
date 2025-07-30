import datetime
from django.core.mail import send_mail
from django.conf import settings
from .models import Membros

# Function to check for birthdays and anniversaries

def check_birthdays_and_anniversaries():
    today = datetime.date.today()
    start_of_week = today - datetime.timedelta(days=today.weekday() + 1)  # Sunday
    end_of_week = start_of_week + datetime.timedelta(days=6)  # Saturday

    # Get members with birthdays this week
    birthdays = Membros.objects.filter(data_nascimento__range=(start_of_week, end_of_week))
    # Get members with anniversaries this week
    anniversaries = Membros.objects.filter(data_casamento__range=(start_of_week, end_of_week))

    # Prepare the email content
    subject = "Aniversários e Casamentos da Semana"
    message = ""

    if birthdays.exists():
        message += "Aniversários:\n"
        for member in birthdays:
            message += f"- {member.nome} ({member.data_nascimento.strftime('%d/%m/%Y')})\n"

    if anniversaries.exists():
        message += "\nCasamentos:\n"
        for member in anniversaries:
            message += f"- {member.nome} ({member.data_casamento.strftime('%d/%m/%Y')})\n"

    if message:
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [settings.NOTIFICATION_EMAIL],
            fail_silently=False,
        )