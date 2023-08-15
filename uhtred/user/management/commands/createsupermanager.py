from typing import Union
from django.core.management.base import BaseCommand

from uhtred.user.models import User


class Command(BaseCommand):

    help = 'Creates a new super manager for django admin site'

    def add_arguments(self, parser):
        parser.add_argument('username',type=str,
            help='Manager username')
        parser.add_argument('password', type=str,
            help='Manager password')
        
    def handle(self, *args, **kwargs):
        
        username: Union[None, str] = kwargs.get('username')
        password: Union[None, str] = kwargs.get('password')
        
        if not User.objects.is_username_registered(username):
            user: User = User.objects.create(
                role=User.Role.MANAGER,
                username=username,
                is_superuser=True,
                is_staff=True)
            user.set_password(password)
            user.save()
            return self.stdout.write(self.style.SUCCESS(f"Successful created super manager {username}"))
        return self.stdout.write(self.style.ERROR(f"Already registered an user with '{username}' username"))
