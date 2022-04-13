from django.core.management import BaseCommand
from django.db.utils import OperationalError
from django.db import connections
import time
from django.utils import timezone
from faker import Faker
from random import randrange, choice
from core.models import Product


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        faker = Faker()

        for _ in range(30):
            title = choice(["GUMINĖ ATRAMA", "AKUMULIATORIUS", "VARŽTAS", "LAIKIKLIS"])
            oem_part_number = str(randrange(100000000, 12345678912))
            brand = choice(["RECONDITION", "BOSH", "WABCO", "EBS", "SAMPA"])
            manufacturer = choice(["MERCEDES", "AUDI", "VOLVO"])
            price = randrange(10.0, 250.0)
            diameter = randrange(10.0, 500.0)
            height = randrange(10.0, 500.0)
            width = randrange(100.0, 600.0)
            weight = randrange(10.0, 2500.0)
            Product.objects.create(
                title=title,
                image=faker.image_url(),
                oem_part_number=oem_part_number,
                brand=brand,
                manufacturer=manufacturer,
                price=price,
                diameter=diameter,
                height=height,
                width=width,
                weight=weight,
                description=( title +
                              " su kaina: " + str(price) + ";" +
                              "\n----MATMENYS----\n*Aukštis: " + str(height) +
                              " \n*Plotis: " + str(width) +
                              " \n*Diametras: " + str(diameter) +
                              " \n*Svoris: " + str(weight)
                            )
            )
        self.stdout.write(self.style.SUCCESS('products loaded!'))
                