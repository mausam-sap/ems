from django.urls import path
from . import views

app_name = 'employees'
urlpatterns = [
    path('', views.employee_list, name='list'),
    path('add/', views.employee_create, name='create'),
    path('<int:pk>/edit/', views.employee_edit, name='edit'),
    path('<int:pk>/delete/', views.employee_delete, name='delete'),
    path('<int:pk>/profile/', views.employee_profile, name='profile'),
    path('departments/', views.department_list, name='departments'),
    path('departments/add/', views.department_create, name='dept_create'),
    path('departments/<int:pk>/edit/', views.department_edit, name='dept_edit'),
    path('departments/<int:pk>/delete/', views.department_delete, name='dept_delete'),
]
