import random
import string

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.views import LoginView as BaseLoginView
from django.contrib.auth.views import LogoutView as BaseLogoutView
from django.core.mail import send_mail
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, View, ListView, DeleteView

from newsletter.models import Message
from users.forms import UserRegisterForm, UserForm, VerificationForm
from users.models import User


class LoginView(BaseLoginView):
    """
    View for user login.
    """
    template_name = 'users/login.html'
    extra_context = {
        'title': 'Log in to account'
    }

    def form_valid(self, form):
        """
        Creates a success message about successful login.
        """
        response = super().form_valid(form)
        messages.success(self.request, 'Вы успешно авторизовались')
        return response


class LogoutView(BaseLogoutView):
    pass


class RegisterView(CreateView):
    """
    View for user registration.
    """
    model = User
    extra_context = {
        'title': 'Registration'
    }
    form_class = UserRegisterForm
    success_url = reverse_lazy('users:login')
    template_name = 'users/register.html'

    def form_valid(self, form):
        """
        Handler called when form is successfully validated.
        Creates a new user, sets their activation status to False, generates a unique verification code,
        saves the user, and sends an email with the verification code to the user's email address.
        """
        user = form.save(commit=False)
        user.is_active = False
        generate_code = ''.join([str(random.randint(0, 9)) for _ in range(12)])
        user.verify_code = generate_code
        user.save()

        # Sending an email with the activation code
        send_mail(
            subject='Код верификации',
            message=f'Пожалуйста, для вашей верификации и активации аккаунта введите код: {generate_code}',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email]
        )
        return redirect(reverse('users:verification', kwargs={'pk': user.pk}))


class UserVerifyView(View):
    """
    View for user verification during registration.
    """
    template_name = 'users/verification.html'
    extra_context = {
        'title': 'Verification'
    }

    def get(self, request, *args, **kwargs):
        form = VerificationForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        """
        Compares the entered code with the one sent to the user's email for verification.
        """
        form = VerificationForm(request.POST)
        if form.is_valid():
            entered_code = form.cleaned_data['verify_code']
            user_pk = kwargs.get('pk')
            user = get_object_or_404(User, pk=user_pk)

            if entered_code == user.verify_code:
                user.is_active = True
                user.save()
                messages.success(request, 'Аккаунт успешно активирован!')
                return redirect(reverse('users:login'))
            else:
                messages.error(request, 'Неверный код верификации. Попробуйте снова.')

        return render(request, self.template_name, {'form': form})


class UserListView(UserPassesTestMixin, ListView):
    """
    View for displaying the list of users.
    """
    model = User
    extra_context = {
        'title': 'Our Users'
    }

    def test_func(self):
        """
        Checks whether the user has manager rights or is a superuser.
        """
        return self.request.user.groups.filter(name='manager').exists() or self.request.user.is_superuser


class GenerateNewPasswordView(View):
    """
    View for generating a new password.
    """

    def generate_random_password(self, length=12):
        """
        Generates a new random password.
        """
        characters = string.ascii_letters + string.digits
        return ''.join(random.choice(characters) for _ in range(length))

    def get(self, request, *args, **kwargs):
        new_password = self.generate_random_password()
        # Send email with the new password
        send_mail(
            subject='Password reset',
            message=f'Your new password: {new_password}\n'
                    f'Login with your new password',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[request.user.email]
        )
        request.user.set_password(new_password)
        request.user.save()
        return redirect(reverse('users:login'))


class UserUpdateView(UpdateView):
    """
    View for editing user data.
    """
    model = User
    extra_context = {
        'title': 'Edit profile'
    }
    success_url = reverse_lazy('users:profile_edit')
    form_class = UserForm

    def get_object(self, queryset=None):
        return self.request.user


class UserDeleteView(DeleteView):
    """
    View for deleting a user.
    """
    model = User
    success_url = reverse_lazy('home:home')
    extra_context = {
        'title': 'Delete account',
    }


class ManagerView(UserPassesTestMixin, View):
    """
    View for the manager interface.
    """
    template_name = 'users/manager.html'

    def get(self, request, *args, **kwargs):
        context = {
            'title': 'Manager account',
        }
        return render(request, self.template_name, context)

    def test_func(self):
        """
         Checks if the user has manager rights or is a superuser.
         """
        return self.request.user.groups.filter(name='manager').exists() or self.request.user.is_superuser


class DisableUserView(UserPassesTestMixin, View):
    """
    View for deactivating (blocking) or activating a user.
    """

    def get(self, request, pk):
        user = User.objects.get(pk=pk)

        if user.is_active:
            user.is_active = False
        elif not user.is_active:
            user.is_active = True

        user.save()
        return redirect('users:users_list')

    def test_func(self):
        """
        Checks if the user has manager rights or is a superuser.
        """
        return self.request.user.groups.filter(name='manager').exists() or self.request.user.is_superuser


class DisableMessageView(UserPassesTestMixin, View):
    """
    View for disabling/enabling a message.
    """

    def get(self, request, pk):
        message = Message.objects.get(pk=pk)

        if message.is_active:
            message.is_active = False
        elif not message.is_active:
            message.is_active = True

        message.save()
        return redirect('newsletter:message_detail', pk=pk)

    def test_func(self):
        """
        Checks if the user has manager rights or is a superuser.
        """
        return self.request.user.groups.filter(name='manager').exists() or self.request.user.is_superuser
