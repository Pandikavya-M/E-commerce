from django.contrib.auth.forms import UserCreationForm
from .models import User
from django import forms

class CustomUserForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form_control','placeholder':'Enter user name'}))
    email = forms.CharField(widget=forms.EmailInput(attrs={'class':'form_control','placeholder':'Enter Email'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form_control','placeholder':'Enter password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form_control','placeholder':'Enter Conform Password'}))
    class Meta:
        model=User
        fields=['username','email','password1','password2']