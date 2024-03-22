from django import forms
from django.contrib.auth.models import User

from .models import Profile


# Create a UserUpdateForm to update your username and email
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
