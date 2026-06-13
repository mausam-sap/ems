from django.contrib import admin
from .models import LeaveRequest

@admin.register(LeaveRequest)
class LeaveAdmin(admin.ModelAdmin):
    list_display = ('employee', 'leave_type', 'start_date', 'end_date', 'status', 'applied_on')
    list_filter = ('status', 'leave_type')
