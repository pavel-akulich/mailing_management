from django import forms

from service_client.models import Client


class ClientForm(forms.ModelForm):
    """
    Form for creating or updating a client.

    Attributes:
        model (Model): The model associated with the form.
        fields (tuple): The fields to be included in the form.
        widgets (dict): Custom widgets for the form fields.
        labels (dict): Custom labels for the form fields.
    """

    class Meta:
        """
        Meta_class configuration for the ClientForm.
        """
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
