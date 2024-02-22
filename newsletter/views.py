from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView

from newsletter.forms import MessageForm
from newsletter.models import Message, MailingLogs


class MessageListView(LoginRequiredMixin, ListView):
    """
    View for displaying the list of messages.

    Attributes:
        model (Model): The model associated with the view.
        ordering (tuple): The default ordering for the queryset.
        extra_context (dict): Extra context data to be included in the view.
    """
    model = Message
    ordering = ('title',)
    extra_context = {
        'title': 'Список рассылок'
    }


class MessageDetailView(LoginRequiredMixin, DetailView):
    """
    View for detailed view of a message.

    Attributes:
        model (Model): The model associated with the view.
        extra_context (dict): Extra context data to be included in the view.
    """
    model = Message
    extra_context = {
        'title': 'Просмотр рассылки'
    }


class MessageCreateView(LoginRequiredMixin, CreateView):
    """
    View for creating a message.

    Attributes:
        model (Model): The model associated with the view.
        form_class (Form): The form class used for the view.
        success_url (str): The URL to redirect to after successful form submission.
        extra_context (dict): Extra context data to be included in the view.
    """
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('newsletter:message_list')

    extra_context = {
        'title': 'Создание рассылки'
    }

    def form_valid(self, form):
        """
        Assigns the current user as the owner of the message.
        """
        form.instance.owner = self.request.user
        return super().form_valid(form)


class MessageUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    View for updating a message.

    Attributes:
        model (Model): The model associated with the view.
        form_class (Form): The form class used for the view.
        extra_context (dict): Extra context data to be included in the view.
    """
    model = Message
    form_class = MessageForm

    extra_context = {
        'title': 'Редактирование рассылки'
    }

    def get_success_url(self):
        """
        Redirects to the detailed view of the message upon success.
        """
        return reverse('newsletter:message_detail', args=[self.kwargs.get('pk')])

    def test_func(self):
        """
        Checks whether the user has the rights of the message owner or is a superuser.
        """
        return self.request.user == self.get_object().owner or self.request.user.is_superuser


class MessageDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    View for deleting a message.

    Attributes:
        model (Model): The model associated with the view.
        success_url (str): The URL to redirect to after successful deletion.
        extra_context (dict): Extra context data to be included in the view.
    """
    model = Message
    success_url = reverse_lazy('newsletter:message_list')

    extra_context = {
        'title': 'Удаление рассылки'
    }

    def test_func(self):
        """
        Checks whether the user has the rights of the message owner or is a superuser.
        """
        return self.request.user == self.get_object().owner or self.request.user.is_superuser


class MailingLogsListView(LoginRequiredMixin, ListView):
    """
    View for viewing mailing logs.

    Attributes:
        model (Model): The model associated with the view.
        extra_context (dict): Extra context data to be included in the view.
    """
    model = MailingLogs
    extra_context = {
        'title': 'Отчет рассылок'
    }

    def get_queryset(self):
        """
        Checks if the user is a superuser or has the right to view all mailings (staff),
        then displays all mailings, otherwise filters by owner and displays only their logs.
        """
        order_by = self.request.GET.get('order_by', '-datetime_attempt')

        if self.request.user.is_superuser or self.request.user.is_staff:
            return MailingLogs.objects.all().order_by(order_by)
        else:
            return MailingLogs.objects.filter(message__owner=self.request.user).order_by(order_by)
