from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView

from service_client.forms import ClientForm
from service_client.models import Client


class ClientCreateView(LoginRequiredMixin, CreateView):
    """
    Контроллер для создания клиента
    """
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('client:client_list')

    extra_context = {
        'title': 'Создание клиента'
    }


class ClientUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    Контроллер для редактирования клиента
    """
    model = Client
    form_class = ClientForm

    extra_context = {
        'title': 'Редактирование клиента'
    }

    def get_success_url(self):
        return reverse('client:client_view', args=[self.kwargs.get('pk')])

    def test_func(self):
        """
        Проверяет, имеет ли пользователь права менеджера или является ли он суперпользователем
        """
        return self.request.user.groups.filter(name='manager').exists() or self.request.user.is_superuser


class ClientListView(LoginRequiredMixin, ListView):
    """
    Контроллер для просмотра списка всех клиентов
    """
    model = Client
    ordering = ('last_name',)
    extra_context = {
        'title': 'Клиенты сервиса'
    }


class ClientDetailView(LoginRequiredMixin, DetailView):
    """
    Контроллер для просмотра деталей клиента
    """
    model = Client
    extra_context = {
        'title': 'Просмотр клиента'
    }


class ClientDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    Контроллер для удаления клиента
    """
    model = Client
    success_url = reverse_lazy('client:client_list')

    extra_context = {
        'title': 'Удаление клиента'
    }

    def test_func(self):
        """
        Проверяет, имеет ли пользователь права менеджера или является ли он суперпользователем
        """
        return self.request.user.groups.filter(name='manager').exists() or self.request.user.is_superuser
