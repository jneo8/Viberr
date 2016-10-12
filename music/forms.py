from django.contrib.auth.models import User
from django import forms
from django.contrib.auth import authenticate, login


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']


class LoginForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Enter Account'}), label='Account')
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'placeholder': 'Enter Password'}))

    class Meta:
        model = User
        fields = ['username', 'password']      