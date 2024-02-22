from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView

from blog.models import Blog


class BlogListView(LoginRequiredMixin, ListView):
    """
    View for displaying a list of blog posts.

    Attributes:
        model (Blog): The model used for the view.
        extra_context (dict): Additional context data for the view.
    """
    model = Blog
    extra_context = {
        'title': 'TechBlog'
    }

    def get_context_data(self, **kwargs):
        """
        Get additional context data.

        Returns:
            dict: Context data for the view.
        """
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['content_manager'] = user.groups.filter(name='content_manager').exists() or user.is_superuser
        return context


class BlogCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    """
    View for creating a new blog post.

    Attributes:
        model (Blog): The model used for the view.
        fields (tuple): Fields to be displayed in the form.
        success_url (str): URL to redirect to upon successful form submission.
        extra_context (dict): Additional context data for the view.
    """
    model = Blog
    fields = ('title', 'content', 'preview')
    success_url = reverse_lazy('blog:blog_list')
    extra_context = {
        'title': 'Add new article',
    }

    def test_func(self):
        """
        Check if the user has the permissions to access the view.

        Returns:
            bool: True if the user has access rights, False otherwise.
        """
        return self.request.user.groups.filter(name='content_manager').exists() or self.request.user.is_superuser


class BlogDetailView(LoginRequiredMixin, DetailView):
    """
    View for displaying details of a blog post.

    Attributes:
        model (Blog): The model used for the view.
        extra_context (dict): Additional context data for the view.
    """
    model = Blog
    extra_context = {
        'title': 'View blog article'
    }

    def get_object(self, queryset=None):
        """
        Get the blog post object. Increases the number of article views.

        Returns:
            Blog: The blog post object.
        """
        self.object = super().get_object(queryset)
        self.object.views_count += 1
        self.object.save()
        return self.object


class BlogUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    View for updating a blog post.

    Attributes:
        model (Blog): The model used for the view.
        fields (tuple): Fields to be displayed in the form.
        success_url (str): URL to redirect to upon successful form submission.
        extra_context (dict): Additional context data for the view.
    """
    model = Blog
    fields = ('title', 'content', 'preview')
    success_url = reverse_lazy('blog:blog_list')
    extra_context = {
        'title': 'Edit article',
    }

    def get_success_url(self):
        """
        Get the URL to redirect to after successful form submission.

        Returns:
            str: The redirect URL.
        """
        return reverse('blog:blog_detail', args=[self.kwargs.get('pk')])

    def test_func(self):
        """
        Check if the user has the permissions to access the view.

        Returns:
            bool: True if the user has access rights, False otherwise.
        """
        return self.request.user.groups.filter(name='content_manager').exists() or self.request.user.is_superuser


class BlogDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    View for deleting a blog post.

    Attributes:
        model (Blog): The model used for the view.
        success_url (str): URL to redirect to upon successful deletion.
        extra_context (dict): Additional context data for the view.
    """
    model = Blog
    success_url = reverse_lazy('blog:blog_list')
    extra_context = {
        'title': 'Delete article',
    }

    def test_func(self):
        """
        Check if the user has the permissions to access the view.

        Returns:
            bool: True if the user has access rights, False otherwise.
        """
        return self.request.user.groups.filter(name='content_manager').exists() or self.request.user.is_superuser
