from django.db import models
from decimal import Decimal
from datetime import datetime
from django.utils import timezone

# Create your models here.

class Applications(models.Model):
    STATUS_CHOICES = ( 
        (1, 'Черновик'), 
        (2, 'Удален'), 
        (3, 'Сформирован'), 
        (4, 'Завершен'), 
        (5, 'Отклонен'), 
    )

    id_creator = models.ForeignKey('Users', on_delete=models.CASCADE, blank=True, null=False)
    id_moderator = models.ForeignKey('Users', on_delete=models.CASCADE, related_name='applications_customer_set', blank=True, null=True)
    status = models.IntegerField(choices=STATUS_CHOICES, null=False)
    creation_date = models.DateTimeField(default=timezone.now, null=False)
    formation_date = models.DateTimeField(blank=True, null=True)
    completion_date = models.DateTimeField(blank=True, null=True)

    class Meta: 
        verbose_name_plural = "Applications" 
        managed = True 

class ApplicationsComponents(models.Model):
    id_component = models.ForeignKey('Components', on_delete=models.CASCADE, blank=True, null=False)
    id_application = models.ForeignKey('Applications', on_delete=models.CASCADE, blank=True, null=False)
    components_amount = models.IntegerField(null=False)

    class Meta:
        managed = True
        unique_together = (('id_component', 'id_application'),)

class Users(models.Model):
    phone_number = models.CharField(max_length=30, null=True)
    adress = models.CharField(max_length=400, null=True)
    is_moderator = models.BooleanField(null=False)
    login = models.CharField(max_length=255, null=False)
    passwd = models.CharField(max_length=255, null=False)

    class Meta: 
        verbose_name_plural = "Users" 
        managed = True

class Components(models.Model):
    STATUS_CHOICES = ( 
        (1, 'Удален'), 
        (2, 'Действует'), 
    )

    price = models.DecimalField(max_digits=19, decimal_places=4, default=Decimal('0.00'), blank=True, null=False)
    weight = models.BigIntegerField(null=False)
    city_production = models.CharField(max_length=100, null=False)
    category = models.CharField(max_length=100, null=False)
    image_path = models.TextField(null=False)
    manufacturing_ccompany = models.CharField(max_length=255, null=False)
    status = models.IntegerField(choices=STATUS_CHOICES, null=False)
    component_name = models.CharField(max_length=255, null=False)
    description = models.TextField(null=False)
    engine_name = models.CharField(max_length=255, blank=True, null=True)
    total_thrust = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    dry_weight = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    combustion_chamber_pressure = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)

    class Meta:
        verbose_name_plural = "Components" 
        managed = True