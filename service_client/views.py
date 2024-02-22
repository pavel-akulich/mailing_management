from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView

from service_client.forms import ClientForm
from service_client.models import Client


class ClientCreateView(LoginRequiredMixin, CreateView):
    """
    View for creating a client.

    Attributes:
        model (Model): The model associated with the view.
        form_class (Form): The form class used for the view.
        success_url (str): The URL to redirect to after successful creation.
        extra_context (dict): Extra context data to be included in the view.
    """
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('client:client_list')

    extra_context = {
        'title': 'Создание клиента'
    }


class ClientUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    View for updating a client.

    Attributes:
        model (Model): The model associated with the view.
        form_class (Form): The form class used for the view.
        extra_context (dict): Extra context data to be included in the view.
    """
    model = Client
    form_class = ClientForm

    extra_context = {
        'title': 'Редактирование клиента'
    }

    def get_success_url(self):
        """
        Redirects to the detailed view of the client upon success.
        """
        return reverse('client:client_view', args=[self.kwargs.get('pk')])

    def test_func(self):
        """
        Checks whether the user has manager rights or is a superuser.
        """
        return self.request.user.groups.filter(name='manager').exists() or self.request.user.is_superuser


class ClientListView(LoginRequiredMixin, ListView):
    """
    View for listing all clients.

    Attributes:
        model (Model): The model associated with the view.
        ordering (tuple): The default ordering for the queryset.
        extra_context (dict): Extra context data to be included in the view.
    """
    model = Client
    ordering = ('last_name',)
    extra_context = {
        'title': 'Клиенты сервиса'
    }


class ClientDetailView(LoginRequiredMixin, DetailView):
    """
    View for detailed view of a client.

    Attributes:
        model (Model): The model associated with the view.
        extra_context (dict): Extra context data to be included in the view.
    """
    model = Client
    extra_context = {
        'title': 'Просмотр клиента'
    }


class ClientDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    View for deleting a client.

    Attributes:
        model (Model): The model associated with the view.
        success_url (str): The URL to redirect to after successful deletion.
        extra_context (dict): Extra context data to be included in the view.
    """
    model = Client
    success_url = reverse_lazy('client:client_list')

    extra_context = {
        'title': 'Удаление клиента'
    }

    def test_func(self):
        """
        Checks whether the user has manager rights or is a superuser.
        """
        return self.request.user.groups.filter(name='manager').exists() or self.request.user.is_superuser
