import random
from datetime import timedelta
from django.utils import timezone


def random_date():
    now = timezone.now()
    return now + timedelta(random.uniform(-1, 0) * 100)


def random_timedelta(factor=100):
    return timedelta(random.uniform(0, 1) * factor)