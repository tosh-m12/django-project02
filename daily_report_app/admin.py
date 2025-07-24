from django.contrib import admin

from django.contrib import admin
from .models import Employee, DailyReport

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('name', 'department', 'email', 'is_active')
    search_fields = ('name', 'department')
    list_filter = ('is_active',)

@admin.register(DailyReport)
class DailyReportAdmin(admin.ModelAdmin):
    list_display = ('date', 'employee', 'inbound', 'outbound', 'shipment', 'canceled')
    list_filter = ('date', 'employee', 'canceled')
    search_fields = ('employee__name',)
