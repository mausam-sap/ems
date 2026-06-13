from django.urls import path
from . import views

app_name = 'reports'
urlpatterns = [
    path('', views.admin_dashboard, name='admin_dashboard'),
]
