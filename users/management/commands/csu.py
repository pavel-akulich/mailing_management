from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):
        user = User.objects.create(
            email='enter_your_email',
            first_name='enter_your_name',
            last_name='enter_your_lastname',
            is_staff=True,
            is_superuser=True
        )

        user.set_password('enter_your_password')
        user.save()
