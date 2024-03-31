from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Profile


# Create a UserUpdateForm to update your username
class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username']


# Creating a ProfileUpdateForm form for adding/updating data
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_pic', 'first_name', 'last_name', 'banner', 'age', 'sex', 'seeking', 'about', 'city',
                  'online_status']


class SignUpForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].error_messages = {
            'required': 'Login can\'t be empty',
            'unique': 'That username has already been taken',
            'invalid': 'Invalid username format',
            'max_length': 'Username is too long',
        }
        self.fields['password1'].error_messages = {
            'required': 'Password can\'t be empty',
            'min_length': 'Password must be at least 8 characters',
        }
        self.fields['password2'].error_messages = {
            'required': 'Confirm Password can\'t be empty',
            'min_length': 'Password must be at least 8 characters',
            'mismatch': 'Password did not match',
        }

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']


class SignUpStepOneForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'age']


class SignUpStepTwoForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['city', 'sex', 'seeking']


class SignUpStepThreeForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_pic', 'about']


class PasswordResetForm(forms.Form):
    new_password = forms.CharField(widget=forms.PasswordInput(), label="New Password")
    confirm_password = forms.CharField(widget=forms.PasswordInput(), label="Confirm Password")
