from django import forms

from newsletter.models import Message
from newsletter.validators import validate_even


class MessageForm(forms.ModelForm):
    """
    Form for creating or updating a message.

    Attributes:
        title (CharField): Title of the message.
        body (CharField): Body of the message.
    """
    title = forms.CharField(validators=[validate_even],
                            label='Название рассылки',
                            widget=forms.TextInput(
                                attrs={
                                    'class': 'form-control',
                                    'placeholder': 'Впишите название',
                                }
                            ))

    body = forms.CharField(validators=[validate_even],
                           label='Содержимое рассылки',
                           widget=forms.Textarea(
                               attrs={
                                   'class': 'form-control',
                                   'placeholder': 'Напишите содержимое рассылки',
                               }
                           ))

    class Meta:
        """
        Meta_class configuration for the MessageForm.
        """
        model = Message
        fields = ('client', 'title', 'body', 'mailing_settings',)
        widgets = {
            'client': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'mailing_settings': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'client': 'Выберите клиентов(Ctrl+C для выбора нескольких)',
            'mailing_settings': 'Выберите настройки для рассылки',
        }
