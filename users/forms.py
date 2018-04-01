from django import forms
from django.contrib.auth.forms import UserCreationForm
from users.models import User
from django.core.exceptions import ValidationError


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


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


class EditProfileForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email',
                  'profile_picture', 'favourite_team']
        exclude = ['password']
        labels = {
            'favourite_team': 'Favourite Team (optional)',
            'profile_picture': 'Profile Picture (optional)',
        }