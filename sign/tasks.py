from celery import shared_task
from twilio.rest import Client
from django.utils.timezone import now
from datetime import timedelta
from django.conf import settings
from .models import Appointment

@shared_task
def send_reminders():
    # Filtrer les rendez-vous dans moins d'une heure sans rappel envoyé
    upcoming_appointments = Appointment.objects.filter(
        date_time__lte=now() + timedelta(hours=1),
        date_time__gt=now(),
        reminder_sent=False
    )
    
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

    for appointment in upcoming_appointments:
        message = f"Bonjour {appointment.user.username}, ceci est un rappel pour votre rendez-vous prévu à {appointment.date_time}."
        try:
            client.messages.create(
                body=message,
                from_=settings.TWILIO_PHONE_NUMBER,
                to=appointment.user.loginers.phone
            )
            # Marquer le rappel comme envoyé
            appointment.reminder_sent = True
            appointment.save()
        except Exception as e:
            print(f"Erreur lors de l'envoi du rappel : {e}")
