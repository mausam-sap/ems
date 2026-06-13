from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from apps.accounts.views import dashboard_redirect
from apps.reports.views import admin_dashboard, employee_dashboard

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('apps.accounts.urls')),
    path('dashboard/', dashboard_redirect, name='dashboard'),
    path('admin-dashboard/', admin_dashboard, name='admin_dashboard'),
    path('employee-dashboard/', employee_dashboard, name='employee_dashboard'),
    path('employees/', include('apps.employees.urls')),
    path('attendance/', include('apps.attendance.urls')),
    path('leave/', include('apps.leave.urls')),
    path('payroll/', include('apps.payroll.urls')),
    path('ai/', include('apps.ai_engine.urls')),
    path('', dashboard_redirect),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
