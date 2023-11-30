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
    template_name = 'users/login.html'
    extra_context = {
        'title': 'Log in to account'
    }


class LogoutView(BaseLogoutView):
    pass


class RegisterView(CreateView):
    """
    Контроллер для регистрации пользователя
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
        Обработчик, вызываемый при успешной валидации формы.
        Создает нового пользователя, устанавливает его статус активации в False и генерирует
        уникальный код верификации. Сохраняет пользователя и отправляет письмо с кодом верификации
        на адрес электронной почты пользователя.
        """
        user = form.save(commit=False)
        user.is_active = False
        generate_code = ''.join([str(random.randint(0, 9)) for _ in range(12)])
        user.verify_code = generate_code
        user.save()

        # Отправляем письмо с кодом активации
        send_mail(
            subject='Код верификации',
            message=f'Пожалуйста, для вашей верификации и активации аккаунта введите код: {generate_code}',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email]
        )
        return redirect(reverse('users:verification', kwargs={'pk': user.pk}))


class UserVerifyView(View):
    """
    Контроллер для верификации пользователя при регистрации
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
        Сверяет, чтобы введённый код совпадал с тем, который отправлен пользователю на почту для верификации
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
    Контроллер для отображения списка пользователей
    """
    model = User
    extra_context = {
        'title': 'Our Users'
    }

    def test_func(self):
        return self.request.user.groups.filter(name='manager').exists() or self.request.user.is_superuser


class GenerateNewPasswordView(View):
    """
    Контроллер для генерации нового пароля
    """

    def generate_random_password(self, length=12):
        """
        Генерирует новый рандомный пароль
        """
        characters = string.ascii_letters + string.digits
        return ''.join(random.choice(characters) for _ in range(length))

    def get(self, request, *args, **kwargs):
        new_password = self.generate_random_password()
        # Отправляем письмо с новым паролем
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
    Контроллер для редактирования данных пользователя
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
    Контроллер для удаления пользователя
    """
    model = User
    success_url = reverse_lazy('home:home')
    extra_context = {
        'title': 'Delete account',
    }


class ManagerView(UserPassesTestMixin, View):
    """
    Контроллер для интерфейса менеджера
    """
    template_name = 'users/manager.html'

    def get(self, request, *args, **kwargs):
        context = {
            'title': 'Manager account',
        }
        return render(request, self.template_name, context)

    def test_func(self):
        return self.request.user.groups.filter(name='manager').exists() or self.request.user.is_superuser


class DisableUserView(UserPassesTestMixin, View):
    """
    Контроллер для деактивации(блокировки) либо активации пользователя
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
        return self.request.user.groups.filter(name='manager').exists() or self.request.user.is_superuser


class DisableMessageView(UserPassesTestMixin, View):
    """
    Контроллер для отключения/включения рассылки
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
        Проверяет, имеет ли пользователь права менеджера или является ли он суперпользователем
        """
        return self.request.user.groups.filter(name='manager').exists() or self.request.user.is_superuser
