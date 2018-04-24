from django import forms
from django.contrib.auth.forms import UserCreationForm
from users.models import User
from django.core.exceptions import ValidationError


# Simple username and password login.
class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


# Favourite team and profile picture options are available alongside default fields when a user registers.
class RegistrationForm(UserCreationForm):
    password1 = forms.CharField(
        label='Choose a Password',
        widget=forms.PasswordInput
    )
    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email',
                  'profile_picture', 'favourite_team', 'password1', 'password2']
        labels = {
            'favourite_team': 'Favourite Team (optional)',
            'profile_picture': 'Profile Picture (optional)',
        }

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            password_error = "Your passwords do not match. Please try again."
            raise ValidationError(password_error)

        return password2

    def save(self, commit=True):
        instance = super(RegistrationForm, self).save()

        return instance


# Password is not required for editing a profile, so leave that field out from the Registration form.
class EditProfileForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email',
                  'address_line_1', 'address_line_2', 'city', 'postcode', 'country',
                  'profile_picture', 'favourite_team', 'is_private']
        exclude = ['password']
        labels = {
            'favourite_team': 'Favourite Team (optional)',
            'profile_picture': 'Profile Picture (optional)',
            'is_private': 'Make Profile Private',
        }


# Password is required to delete a user's account.
class DeletionForm(forms.ModelForm):

    password = forms.CharField(
        widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = ['password']

    def clean_password(self):
        password = self.cleaned_data.get('password')

        return password


# Old password is needed to make a change, new password must then be entered and confirmed.
class ChangePasswordForm(forms.ModelForm):
    password1 = forms.CharField(
        label='Choose New Password',
        widget=forms.PasswordInput
    )
    password2 = forms.CharField(
        label='Confirm New Password',
        widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = ['password', 'password1', 'password2']
        labels = {
            'password': 'Current Password',
        }
        widgets = {
            'password': forms.PasswordInput
        }

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            password_error = "Your passwords do not match. Please try again."
            raise ValidationError(password_error)

        return password2
