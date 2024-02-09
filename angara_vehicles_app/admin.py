from django.contrib import admin

from .models import Components
from .models import Applications
from .models import Users
from .models import ApplicationsComponents

# Register your models here.
admin.site.register(Components)
admin.site.register(Applications)
admin.site.register(Users)
admin.site.register(ApplicationsComponents)