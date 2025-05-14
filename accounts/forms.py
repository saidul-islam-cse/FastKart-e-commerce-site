from django.contrib.auth.forms import UserCreationForm
from .import models

class CustomUserRegistrationForms(UserCreationForm):
    class Meta:
        model = models.CustomUser
        fields = ['first_name', 'last_name', 'email', 'password1', 'password2']