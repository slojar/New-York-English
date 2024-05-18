from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from home.models import *


class LoginForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)


class RegistrationForm(forms.Form):
    email = forms.EmailField(help_text='Required. Input a valid email address.', required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    password = forms.CharField(required=True)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password')

    def save(self, commit=True):
        email = self.cleaned_data.get('email').lower()
        first_name = self.cleaned_data.get('first_name')
        last_name = self.cleaned_data.get('last_name')
        password2 = self.cleaned_data.get('password')
        # dob = self.cleaned_data.get('dob')

        user, user_created = User.objects.get_or_create(username=email)
        user.email = email
        user.first_name = first_name
        user.last_name = last_name
        user.password = make_password(password2)
        user.save()

        profile, profile_created = UserProfile.objects.get_or_create(user=user)
        # profile.dob = dob
        profile.save()

        return user


# class ContactForm(forms.ModelForm):
#     class Meta:
#         model = Contact
#         exclude = []


# class SetNewPasswordForm(PasswordChangeForm):
#     class Meta:
#         model = User
#         exclude = []



