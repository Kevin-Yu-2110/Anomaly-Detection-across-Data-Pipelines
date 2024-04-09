from django import forms
from django.contrib.auth.forms import UserCreationForm
from backend_api.models import StandardUser

class SignUpForm(UserCreationForm):
    email = forms.EmailField()
    cc_num = forms.CharField(required=False)

    class Meta:
        model = StandardUser
        fields = ('username', 'email', 'cc_num', 'password1', 'password2')
