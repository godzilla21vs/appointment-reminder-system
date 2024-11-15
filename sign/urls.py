from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('otp_send/<str:phone_number>/', views.otp_send, name='otp_send'),
    path('otp_verify/', views.otp_verify, name='otp_verify'),
    path('create_appointment/', views.create_appointment, name='create_appointment'),
    path('logout/', views.logout, name='logout'),
    
]