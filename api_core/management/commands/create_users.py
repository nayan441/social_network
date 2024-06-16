from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db import IntegrityError

User = get_user_model()
class Command(BaseCommand):
    help = 'Create 10 users in the database'

    def handle(self, *args, **kwargs):
        for i in range(10):
            name = f'user{i+1}'
            email = f'user{i+1}@gmail.com'
            password = "Qwerty@12345"
            try:
                User.objects.create_user(name=name, email=email, password=password)
                self.stdout.write(self.style.SUCCESS(f'Successfully created user\n --> email : user{i+1}@gmail.com\n --> password : Qwerty@12345'))
            except IntegrityError:
                self.stdout.write(self.style.ERROR(f'Error: User {name} or email {email} already exists'))



