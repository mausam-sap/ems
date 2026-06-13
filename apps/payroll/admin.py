from django.contrib import admin
from .models import PayrollRecord

@admin.register(PayrollRecord)
class PayrollAdmin(admin.ModelAdmin):
    list_display = ('employee', 'month', 'year', 'net_salary', 'generated_on')
    list_filter = ('year', 'month')
