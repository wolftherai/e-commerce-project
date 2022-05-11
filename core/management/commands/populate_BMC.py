from django.core.management import BaseCommand
from core.models import Manufacturer, Brand, Category


class Command(BaseCommand):
    def handle(self, *args, **kwargs):

        for manufacturer in ["MERCEDES", "AUDI", "VOLVO", "RENAULT"]:
            Manufacturer.objects.create(
                name=manufacturer,
            )
        self.stdout.write(self.style.SUCCESS('Manufacturers loaded!'))

        for brand in ["RECONDITION", "BOSH", "WABCO", "EBS", "SAMPA"]:
            Brand.objects.create(
                name=brand,
            )
        self.stdout.write(self.style.SUCCESS('Brands loaded!'))

        for category in ["KĖBULAS", "FILTRAI", "VAIRO MECHANIZMAS", "KURO SISTEMA", "APŠVIETIMO SISTEMA", "TRANSMISIJOS SISTEMA", "PADANGOS", "SALONAS IR APDAILA", "PAKABA", "VARIKLIS", "IŠMETIMO SISTEMA"]:
            Category.objects.create(
                name=category,
            )
        self.stdout.write(self.style.SUCCESS('Categories loaded!'))
