from django.contrib import admin

# Register your models here.
from .models import Period, User


admin.site.register(Period)
admin.site.register(User)
