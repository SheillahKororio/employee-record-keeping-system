from django.contrib import admin
from .models import Employee


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ("eid", "ename", "eemail", "econtact")
    search_fields = ("eid", "ename", "eemail", "econtact")
    ordering = ("ename",)
