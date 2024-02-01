from django.contrib import admin
from .models import *

admin.site.register(Vehicle)
admin.site.register(VehicleOrder)
admin.site.register(Order)
admin.site.register(CustomUser)

