from django.urls import path
from . import views

app_name = 'ai'
urlpatterns = [
    path('', views.ai_dashboard, name='dashboard'),
    path('run/', views.run_predictions, name='run'),
    path('employee/<int:pk>/', views.employee_prediction, name='employee'),
    path('my/', views.my_prediction, name='my'),
]
