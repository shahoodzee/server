from django.contrib import admin
from .models import Task,Address
# Register your models here.
admin.site.register(Address)
admin.site.register(Task)
