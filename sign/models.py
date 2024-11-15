from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField

class Loginers(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = PhoneNumberField(unique=True)
    
    def __str__(self):
        return self.user.username

class Appointment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_time = models.DateTimeField()
    reminder_sent = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.user.username} - {self.date_time}"

