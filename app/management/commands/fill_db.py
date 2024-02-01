import random

from django.core import management
from django.core.management.base import BaseCommand
from ...models import *
from .utils import random_date, random_timedelta


def add_vehicles():
    Vehicle.objects.create(
        name="Титановый шаробалонн",
        category="Дополнительные запчасти",
        description="В августе 2018 года было сообщено, что первая товарная партия титановых шаробаллонов (ТШБ) для ракет-носителей «Ангара» отправлена с Воронежского механического завода (ВМЗ) в ПО «Полёт». Это первый комплект ТШБ российского производства: до 2014 года для российских ракет-носителей их поставлял завод «Южмаш» (Украина).",
        image="vehicles/1.png",
        price=random.randint(10, 100)
    )
    Vehicle.objects.create(
        name="Разгонный блок 'Бриз-М'",
        category="Разгонные блоки",
        description="В качестве верхней ступени предусмотрено применение разгонных блоков: «Бриз-КМ», «Бриз-М», кислородно-водородный среднего класса (КВСК) и кислородно-водородный тяжёлого класса (КВТК).",
        image="vehicles/2.png",
        price=random.randint(10, 100)
    )
    Vehicle.objects.create(
        name="Центральная вычислительная машина 'Бисер-6'",
        category="Электроника",
        description="«Бисер-6» предназначен для управления движением и бортовыми системами, а также для контроля полёта и формирования телеметрической информации. При решении задач навигации и наведения с помощью «Бисера-6» выполняются арифметические и логические операции, а также операции обмена информацией с внешними абонентами.",
        image="vehicles/3.png",
        price=random.randint(10, 100)
    )
    Vehicle.objects.create(
        name="Боковой ракетный модуль - урм 1",
        category="Универсальные ракетные модули",
        description="Носитель тяжелого класса «Ангара-5А» имеет первую ступень, образованную из пяти блоков на основе универсального ракетного модуля. Пять двигателей первой ступени запускаются при старте ракеты одновременно.",
        image="vehicles/4.png",
        price=random.randint(10, 100)
    )
    Vehicle.objects.create(
        name="Центральный ракетный модуль",
        category="Универсальные ракетные модули",
        description="В основу семейства носителей «Ангара» положен универсальный ракетный модуль (УРМ). В его состав входит блок баков окислителя, горючего и двигатель РД-191.",
        image="vehicles/5.png",
        price=random.randint(10, 100)
    )
    Vehicle.objects.create(
        name="Головной обтекатель",
        category="Головные модули",
        description="Задача головных обтекателей ракет-носителей – на момент старта и до вывода в космическое пространство – это защита космического аппарата от всех внешних факторов. Максимальной температурой головного обтекателя считается 175 градусов Цельсия по поверхности.",
        image="vehicles/6.png",
        price=random.randint(10, 100)
    )
    Vehicle.objects.create(
        name="Вторая ступень - универсальный ракетный модуль 2",
        category="Универсальные ракетные модули",
        description="В качестве второй ступени рассматривается либо ступень на компонентах кислород-керосин, аналогичная применяемой на носителе «Ангара-1.2», но с увеличенным запасом компонентов топлива, либо универсальный кислородно-водородный блок («УКВБ»).",
        image="vehicles/7.png",
        price=random.randint(10, 100)
    )

    print("Услуги добавлены")


def add_orders():
    users = CustomUser.objects.filter(is_superuser=False)
    moderators = CustomUser.objects.filter(is_superuser=True)

    if len(users) == 0 or len(moderators) == 0:
        print("Заявки не могут быть добавлены. Сначала добавьте пользователей с помощью команды add_users")
        return

    vehicles = Vehicle.objects.all()

    for _ in range(30):
        order = Order.objects.create()
        order.name = "Заявка №" + str(order.pk)
        order.status = random.randint(2, 5)
        order.owner = random.choice(users)

        if order.status in [2, 3, 4]:
            order.weight = random.randint(100, 1000)

        if order.status in [3, 4]:
            order.date_complete = random_date()
            order.date_formation = order.date_complete - random_timedelta()
            order.date_created = order.date_formation - random_timedelta()
            order.moderator = random.choice(moderators)
        else:
            order.date_formation = random_date()
            order.date_created = order.date_formation - random_timedelta()

        for i in range(random.randint(1, 3)):
            try:
                item = VehicleOrder.objects.create()
                item.order = order
                item.vehicle = random.choice(vehicles)
                item.count = random.randint(1, 3)
                item.save()
            except Exception as e:
                print(e)

        order.save()

    print("Заявки добавлены")


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        management.call_command("clean_db")
        management.call_command("add_users")

        add_vehicles()
        add_orders()









