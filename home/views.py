from django.views.generic import TemplateView
from random import sample
from blog.models import Blog
from home.services import get_cached_clients
from newsletter.models import Message


class HomeView(TemplateView):
    """
    Контроллер отображения домашней страницы
    """
    template_name = 'home/home.html'
    extra_context = {
        'title': 'Mailing Wave'
    }

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['all_messages'] = Message.objects.all()
        context_data['active_messages'] = Message.objects.filter(is_active=True)
        context_data['all_clients'] = get_cached_clients()
        context_data['articles'] = sample(list(Blog.objects.all()), 3)
        return context_data
