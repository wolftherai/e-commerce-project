from django.core.management import BaseCommand
from django_redis import get_redis_connection

from core.models import User


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        con = get_redis_connection("default")

        managers = User.objects.filter(is_manager=True)

        for manager in managers:
            con.zadd('rankings', {manager.name:  float(manager.revenue)})  # added sorted sets to Redis

        self.stdout.write(self.style.SUCCESS('managers loaded!'))