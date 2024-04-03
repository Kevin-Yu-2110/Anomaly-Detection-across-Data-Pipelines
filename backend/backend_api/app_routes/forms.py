from django import forms
from django.contrib.auth.forms import UserCreationForm
from backend_api.models import StandardUser

class SignUpForm(UserCreationForm):
    email = forms.EmailField()
    cc_num = forms.CharField(required=False)
    city = forms.CharField(max_length=100)
    job = forms.CharField(max_length=100)
    dob = forms.DateField()


    class Meta:
        model = StandardUser
        fields = ('username', 'email', 'cc_num', 'city', 'job', 'dob', 'password1', 'password2')
