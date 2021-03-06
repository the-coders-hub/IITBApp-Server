__author__ = 'dheerendra'

from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(
        help_text='Enter Username',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'id': 'username',
                'placeholder': 'LDAP Username'
            }
        ),
        required=True,
        error_messages={
            'required': 'username is required'
        }
    )

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'id': 'password',
                'placeholder': 'Enter Password'
            }
        ),
        required=True,
        error_messages={
            'required': 'password is required'
        }
    )