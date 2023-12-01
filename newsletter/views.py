from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView

from newsletter.forms import MessageForm
from newsletter.models import Message, MailingLogs


class MessageListView(LoginRequiredMixin, ListView):
    """
    Контроллер отображения списка рассылок
    """
    model = Message
    ordering = ('title',)
    extra_context = {
        'title': 'Список рассылок'
    }


class MessageDetailView(LoginRequiredMixin, DetailView):
    """
    Контроллер для детального просмотра рассылки
    """
    model = Message
    extra_context = {
        'title': 'Просмотр рассылки'
    }


class MessageCreateView(LoginRequiredMixin, CreateView):
    """
    Контроллер для создания рассылки
    """
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('newsletter:message_list')

    extra_context = {
        'title': 'Создание рассылки'
    }

    def form_valid(self, form):
        """
        Присваивает текущего пользователя владельцем сообщения
        """
        form.instance.owner = self.request.user
        return super().form_valid(form)


class MessageUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    Контроллер для редактирования рассылки
    """
    model = Message
    form_class = MessageForm

    extra_context = {
        'title': 'Редактирование рассылки'
    }

    def get_success_url(self):
        """
        В случае успеха делает редирект на детальный просмотр рассылки
        """
        return reverse('newsletter:message_detail', args=[self.kwargs.get('pk')])

    def test_func(self):
        """
        Проверяет, имеет ли пользователь права владельца рассылки или является ли он суперпользователем
        """
        return self.request.user == self.get_object().owner or self.request.user.is_superuser


class MessageDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    Контроллер для удаления рассылки
    """
    model = Message
    success_url = reverse_lazy('newsletter:message_list')

    extra_context = {
        'title': 'Удаление рассылки'
    }

    def test_func(self):
        """
        Проверяет, имеет ли пользователь права владельца рассылки или является ли он суперпользователем
        """
        return self.request.user == self.get_object().owner or self.request.user.is_superuser


class MailingLogsListView(LoginRequiredMixin, ListView):
    """
    Контроллер для просмотра логов рассылки
    """
    model = MailingLogs
    extra_context = {
        'title': 'Отчет рассылок'
    }

    def get_queryset(self):
        """
        Проверяет, что пользователь является суперпользователем или имеет право просматривать все рассылки(персонал),
        тогда отобразит все рассылки, в ином случае фильтруем по владельцу и отображаем только его логи
        """
        if self.request.user.is_superuser or self.request.user.is_staff:
            return MailingLogs.objects.all()
        else:
            return MailingLogs.objects.filter(message__owner=self.request.user)
