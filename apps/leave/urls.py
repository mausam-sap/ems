from django.urls import path
from . import views

app_name = 'leave'
urlpatterns = [
    path('', views.leave_list, name='list'),
    path('apply/', views.leave_apply, name='apply'),
    path('<int:pk>/review/', views.leave_review, name='review'),
    path('<int:pk>/cancel/', views.leave_cancel, name='cancel'),
]
