from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):
    """
    Management command to create a superuser.

    This command creates a superuser with the provided email, first name, last name, and password.

    Attributes:
        User (Model): The User model used for creating the superuser.
    """

    def handle(self, *args, **options):
        """
        Executes the command to create a superuser.

        Args:
            args: Command line arguments.
            options: Command line options.
        """
        user = User.objects.create(
            email='enter_your_email',
            first_name='enter_your_name',
            last_name='enter_your_lastname',
            is_staff=True,
            is_superuser=True
        )

        user.set_password('enter_your_password')
        user.save()
