
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate
from phonenumber_field.widgets import PhoneNumberPrefixWidget
from phonenumber_field.formfields import PhoneNumberField


class RegisterForm(forms.ModelForm):
    phonenumber = PhoneNumberField(
       widget=PhoneNumberPrefixWidget(
            # 'widgets' argument specifies the form fields for country code and phone number
            widgets={
                'country': forms.Select(attrs={'class': 'form-control'}),  # Country selection
                'number': forms.TextInput(attrs={'class': 'form-control'})  # Phone number input
            }
        ),
        label="Numéro de téléphone",
        initial='+237'  # Use the correct country code for Cameroon
    )
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), label="Mot de passe")
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), label="Confirmez le mot de passe")

    class Meta:
        model = User
        fields = ['username', 'password', 'phonenumber']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        
        if password != confirm_password:
            raise ValidationError("Les mots de passe ne correspondent pas.")

        return cleaned_data

class LoginForm(forms.Form):
    username = forms.CharField(label="Nom d'utilisateur")
    password = forms.CharField(widget=forms.PasswordInput, label="Mot de passe")

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")
        user = authenticate(username=username, password=password)
        if not user:
            raise ValidationError("Nom d'utilisateur ou mot de passe incorrect.")
        return cleaned_data
