from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Loan

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class LoanForm(forms.ModelForm):
    class Meta:
        model = Loan
        fields = ['amount']