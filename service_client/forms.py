from django import forms

from service_client.models import Client


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ('first_name', 'last_name', 'patronymic', 'email', 'comment')
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Впишите имя'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Впишите фамилию'}),
            'patronymic': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Впишите отчество'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Впишите email'}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Оставьте комментарий'}),
        }

        labels = {
            'patronymic': 'Отчество(если таковое имеется)',
            'comment': 'Комментарий(опционально)',
        }
