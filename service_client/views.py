from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, DetailView, TemplateView, UpdateView, DeleteView

from service_client.models import Client


class HomeView(TemplateView):
    template_name = 'service_client/home.html'
    extra_context = {
        'title': 'Mailing management'
    }


class ClientCreateView(CreateView):
    model = Client
    fields = ('first_name', 'last_name', 'patronymic', 'email', 'comment',)

    success_url = reverse_lazy('client:client_list')

    extra_context = {
        'title': 'Создание клиента'
    }


class ClientUpdateView(UpdateView):
    model = Client
    fields = ('first_name', 'last_name', 'patronymic', 'email', 'comment',)

    extra_context = {
        'title': 'Редактирование клиента'
    }

    def get_success_url(self):
        return reverse('client:client_view', args=[self.kwargs.get('pk')])


class ClientListView(ListView):
    model = Client
    ordering = ('last_name',)
    extra_context = {
        'title': 'Клиенты сервиса'
    }


class ClientDetailView(DetailView):
    model = Client
    extra_context = {
        'title': 'Просмотр клиента'
    }


class ClientDeleteView(DeleteView):
    model = Client
    success_url = reverse_lazy('client:client_list')

    extra_context = {
        'title': 'Удаление клиента'
    }
