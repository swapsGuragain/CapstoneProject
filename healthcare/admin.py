from django.contrib import admin
from .models import Patient, User

# Register your models here.

admin.site.register(Patient)
admin.site.register(User)