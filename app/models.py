from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import PermissionsMixin


class Vehicle(models.Model):
    STATUS_CHOICES = (
        (1, 'Действует'),
        (2, 'Удалена'),
    )

    name = models.CharField(verbose_name="Название", blank=True, null=True)
    category = models.CharField(verbose_name="Категория", blank=True, null=True)
    description = models.TextField(verbose_name="Описание", blank=True, null=True)
    price = models.TextField(verbose_name="Цена", blank=True, null=True)

    status = models.IntegerField( verbose_name="Статус", choices=STATUS_CHOICES, default=1)
    image = models.ImageField(verbose_name="Картинка", default="vehicles/default.png", upload_to="vehicles", blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Комплектующее"
        verbose_name_plural = "Комплектующие"


class CustomUserManager(BaseUserManager):
    def create_user(self, name, email, password="1234", **extra_fields):
        extra_fields.setdefault('name', name)
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, name, email, password="1234", **extra_fields):
        extra_fields.setdefault('is_moderator', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(name, email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=30)
    is_moderator = models.BooleanField(default=False)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class Order(models.Model):
    STATUS_CHOICES = (
        (1, 'Введён'),
        (2, 'В работе'),
        (3, 'Завершен'),
        (4, 'Отклонен'),
        (5, 'Удален'),
    )

    weight = models.IntegerField(verbose_name="Фактическая масса", blank=True, null=True)

    status = models.IntegerField(verbose_name="Статус", choices=STATUS_CHOICES, default=1)
    date_created = models.DateTimeField(verbose_name="Дата создания", default=timezone.now())
    date_formation = models.DateTimeField(verbose_name="Дата формирования", blank=True, null=True)
    date_complete = models.DateTimeField(verbose_name="Дата завершения", blank=True, null=True)

    owner = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING, verbose_name="Создатель", related_name='owner', null=True)
    moderator = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING, verbose_name="Модератор", related_name='moderator', null=True)

    def __str__(self):
        return "Заявка №" + str(self.pk)

    class Meta:
        verbose_name = "Заявка"
        verbose_name_plural = "Заявки"
        ordering = ('-date_formation', )


# м-м
class VehicleOrder(models.Model):
    vehicle = models.ForeignKey(Vehicle, models.CASCADE, blank=True, null=True)
    order = models.ForeignKey(Order, models.CASCADE, blank=True, null=True)
    amount = models.IntegerField(verbose_name="Количество", blank=True, null=True)

    def __str__(self):
        return "Ракетоноситель-Заявка №" + str(self.pk)

    class Meta:
        verbose_name = "Ракетоноситель-Заявка"
        verbose_name_plural = "Ракетоносители-Заявки"
