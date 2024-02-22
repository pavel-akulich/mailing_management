from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms

from users.models import User


class UserRegisterForm(UserCreationForm):
    """
    Form for registering a new user.

    Attributes:
        password1 (CharField): The first password input field.
        password2 (CharField): The second password input field for confirmation.
        model (Model): The model associated with the form.
        fields (tuple): The fields to be included in the form.
        widgets (dict): Custom widgets for the form fields.
    """
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Впишите пароль'}),
        label='Пароль')
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Повторите ваш пароль'}),
        label='Повторите пароль')

    class Meta:
        """
        Meta_class configuration for the UserRegisterForm.
        """
        model = User
        fields = ('email', 'password1', 'password2',)

        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Впишите email'}),
        }


class UserForm(UserChangeForm):
    """
    Form for updating user information.

    Attributes:
        model (Model): The model associated with the form.
        fields (tuple): The fields to be included in the form.
        widgets (dict): Custom widgets for the form fields.
    """

    class Meta:
        """
        Meta_class configuration for the UserForm.
        """
        model = User
        fields = ('email', 'password', 'first_name', 'last_name', 'avatar', 'phone', 'country',)

        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Впишите email'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Впишите имя'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Впишите фамилию'}),
            'avatar': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Впишите номер телефона'}),
            'country': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Впишите страну'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['password'].widget = forms.HiddenInput()


class VerificationForm(forms.Form):
    """
    Form for verification code input.

    Attributes:
        verify_code (CharField): The field for entering the verification code.
    """

    verify_code = forms.CharField(max_length=12, label='Введите код верификации')
