from django.core.management import BaseCommand
from django.db.utils import OperationalError
from django.db import connections
import time
from django.utils import timezone

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        self.stdout.write('waiting for the database...')
        conn = None
        
        while not conn:
            try:
                conn = connections['default']
            except OperationalError:
                self.stdout.write('Database unavailable, waiting for 1 second...')
                time.sleep(1)
                
        self.stdout.write(self.style.SUCCESS('Database available!'))
                