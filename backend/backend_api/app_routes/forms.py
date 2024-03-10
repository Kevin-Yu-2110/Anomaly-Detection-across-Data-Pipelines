from django import forms
from django.contrib.auth.forms import UserCreationForm
from backend_api.models import StandardUser

class SignUpForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = StandardUser
        fields = ('username', 'email', 'password1', 'password2', 'accountType')
