from django.urls import path
from . import views

app_name = 'attendance'
urlpatterns = [
    path('', views.attendance_list, name='list'),
    path('mark/', views.attendance_mark, name='mark'),
    path('bulk/', views.bulk_attendance, name='bulk'),
    path('my/', views.my_attendance, name='my'),
    path('employee/<int:pk>/', views.employee_attendance_report, name='employee_report'),
]
