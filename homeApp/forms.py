from django import forms
from django.contrib.auth.models import User
from homeApp.models import UserSignUp

class SignUpForm(forms.ModelForm):
    class Meta:
        model=UserSignUp
        fields=('username','password','first_name','last_name','email','phonenumber')
