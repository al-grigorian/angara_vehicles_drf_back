from django.core.management.base import BaseCommand
from ...models import *


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        VehicleOrder.objects.all().delete()
        Order.objects.all().delete()
        Vehicle.objects.all().delete()
        CustomUser.objects.all().delete()