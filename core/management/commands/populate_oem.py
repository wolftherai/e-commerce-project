from django.core.management import BaseCommand
from django.db.utils import OperationalError
from django.db import connections
import time
from django.utils import timezone
from faker import Faker
from random import randrange, choice
from core.models import OemPart, CarModel


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        # faker = Faker()

        for _ in range(50):
            first_identifier = choice(["A", "X", "B", "Q"])
            oem_part_number = first_identifier + str(randrange(100000000, 12345678912))

            oem = OemPart.objects.create(
                code=oem_part_number
            )
            print(oem.code)
            models = []
            car_model_id_start = randrange(1, 1747 - 50)
            for car_model_id in range(car_model_id_start, car_model_id_start + 50):
                print(car_model_id)
                models.append(car_model_id)#CarModel.objects.filter(id=car_model_id))
               # oem.car_model.set(CarModel.objects.filter(id=car_model_id)) #.filter(id<car_model_id_end)
              #  oem.save()
            print(len(models))
            oem.car_model.set(models)
            oem.save()
        self.stdout.write(self.style.SUCCESS('OEM codes with carModels loaded!'))
