from django.core.management import BaseCommand
from django.db.utils import OperationalError
from django.db import connections
import time
from django.utils import timezone
from faker import Faker

from core.models import User


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        faker = Faker()

        for _ in range(30):
            user = User.objects.create(
                first_name=faker.first_name(),
                last_name=faker.last_name(),
                email=faker.email(),
                password='',  #faker.password(),
                is_manager=True
            )
            user.set_password('1234')
            user.save()
        self.stdout.write(self.style.SUCCESS('managers loaded!'))
                