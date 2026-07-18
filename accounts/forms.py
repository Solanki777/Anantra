from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    college_name = forms.CharField(max_length=200)
    phone = forms.CharField(max_length=15)
    address = forms.CharField(widget=forms.Textarea)
    city = forms.CharField(max_length=100)
    state = forms.CharField(max_length=100)

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "password1",
            "password2",
            "college_name",
            "phone",
            "address",
            "city",
            "state",
        ]