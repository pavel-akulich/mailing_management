from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView

from blog.models import Blog


class BlogListView(LoginRequiredMixin, ListView):
    """
    Контроллер для отображения всех(списка) статей блога
    """
    model = Blog
    extra_context = {
        'title': 'TechBlog'
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['content_manager'] = user.groups.filter(name='content_manager').exists() or user.is_superuser
        return context


class BlogCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    """
    Контроллер для создания статей блога
    """
    model = Blog
    fields = ('title', 'content', 'preview')
    success_url = reverse_lazy('blog:blog_list')
    extra_context = {
        'title': 'Add new article',
    }

    def test_func(self):
        """
        Проверяет, имеет ли пользователь права контент-менеджера или является ли он суперпользователем
        """
        return self.request.user.groups.filter(name='content_manager').exists() or self.request.user.is_superuser


class BlogDetailView(LoginRequiredMixin, DetailView):
    """
    Контроллер для детального отображения статей блога
    """
    model = Blog
    extra_context = {
        'title': 'View blog article'
    }

    def get_object(self, queryset=None):
        """
        Получает объект из запроса и увеличивает счетчик просмотров
        """
        self.object = super().get_object(queryset)
        self.object.views_count += 1
        self.object.save()
        return self.object


class BlogUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    Контроллер для редактирования статей блога
    """
    model = Blog
    fields = ('title', 'content', 'preview')
    success_url = reverse_lazy('blog:blog_list')
    extra_context = {
        'title': 'Edit article',
    }

    def get_success_url(self):
        """
        В случае успешного редактирования объекта сделает редирект на детальный просмотр этого объекта
        """
        return reverse('blog:blog_detail', args=[self.kwargs.get('pk')])

    def test_func(self):
        return self.request.user.groups.filter(name='content_manager').exists() or self.request.user.is_superuser


class BlogDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    Контроллер для удаления статей блога
    """
    model = Blog
    success_url = reverse_lazy('blog:blog_list')
    extra_context = {
        'title': 'Delete article',
    }

    def test_func(self):
        return self.request.user.groups.filter(name='content_manager').exists() or self.request.user.is_superuser
