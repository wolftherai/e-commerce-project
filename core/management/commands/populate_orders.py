from django.core.management import BaseCommand
from django.db.utils import OperationalError
from django.db import connections
import time
from django.utils import timezone
from faker import Faker
from random import randrange, choice
from core.models import Order, OrderItem


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        faker = Faker()

        for _ in range(3):
            order = Order.objects.create(
                user_id=33,
                code='code',
                manager_email='aaa@a.com',
                first_name=faker.first_name(),
                last_name=faker.last_name(),
                email=faker.email(),
                complete=True
            )

            for _ in range(randrange(1, 5)):
                price = randrange(10, 100)
                quantity = randrange(1, 5)
                OrderItem.objects.create(
                    order_id=order.id,
                    product_title=faker.name(),
                    price=price,
                    quantity=quantity,
                    admin_revenue=.9 * price * quantity,
                    manager_revenue=.1 * price * quantity
                )

        self.stdout.write(self.style.SUCCESS('Orders loaded!'))
                