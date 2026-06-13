from django.urls import path
from . import views

app_name = 'payroll'
urlpatterns = [
    path('', views.payroll_list, name='list'),
    path('generate/', views.generate_payroll, name='generate'),
    path('<int:pk>/', views.payslip_detail, name='detail'),
    path('<int:pk>/pdf/', views.payslip_pdf, name='pdf'),
    path('my/', views.my_payroll, name='my'),
]
