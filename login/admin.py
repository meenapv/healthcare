from django.contrib import admin

# Register your models here.
from .models import UserRole
from .models import Leave

admin.site.register(UserRole)
admin.site.register(Leave)