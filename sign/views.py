from django.contrib import messages
from django.shortcuts import redirect, render
from requests import request
from twilio.rest import Client
from django.http import JsonResponse
import random

from django.shortcuts import render
from django.utils import timezone
from .models import Appointment

from .forms import *
from django.contrib.auth import login as auth_login, authenticate

from django.conf import settings
from django.contrib.auth import logout as auth_logout
import requests

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])
            user.save()
            Loginers.objects.create(user=user, phone=form.cleaned_data["phonenumber"])
            messages.success(request, "Inscription réussie. Vous pouvez maintenant vous connecter.")
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=username, password=password)
            if user:
                auth_login(request, user)
                return redirect('otp_send', phone_number=user.loginers.phone)
            else:
                messages.error(request, "Nom d'utilisateur ou mot de passe incorrect.")
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def otp_send(request, phone_number):
    otp = random.randint(10000, 99999)
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    try:
        client.messages.create(
            body=f"Votre code OTP est {otp}",
            from_=settings.TWILIO_PHONE_NUMBER,
            to=phone_number
        )
        request.session['otp'] = otp  # Sauvegarde temporaire du code OTP
        return render(request, 'otp_verify.html', {'phone_number': phone_number})
    except Exception as e:
        messages.error(request, f"Erreur d'envoi de l'OTP : {e}")
        return redirect('login')



def otp_verify(request):
    if request.method == 'POST':
        otp_input = request.POST.get('otp')
        if int(otp_input) == request.session.get('otp'):
            del request.session['otp']
            messages.success(request, "Connexion réussie.")
            return redirect('home')
        else:
            messages.error(request, "Code OTP incorrect.")
            return redirect('otp_verify')
    return render(request, 'otp_verify.html')


def create_appointment(request):
    if request.method == 'POST':
        appointment_time = request.POST.get('appointment_time')
        user = request.user
        appointment = Appointment.objects.create(user=user, date_time=appointment_time)
        messages.success(request, "Rendez-vous créé avec succès.")
        return render(request, 'appointment_success.html')
    return render(request, 'appointment_creation.html')

def logout(request):
    auth_logout(request)
    messages.success(request, "Déconnexion réussie.")
    return redirect('login')