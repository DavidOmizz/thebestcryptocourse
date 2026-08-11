from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):
    """
    Django's built-in UserCreationForm only asks for username + password.
    We add email too, since that's how you'll recognise a buyer when they
    email their payment proof.
    """
    email = forms.EmailField(required=True, help_text="Use the email you'll send your payment proof from.")

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
