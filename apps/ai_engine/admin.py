from django.contrib import admin
from .models import PerformancePrediction, AbsenteeismPrediction

@admin.register(PerformancePrediction)
class PerfAdmin(admin.ModelAdmin):
    list_display = ('employee', 'predicted_score', 'risk_label', 'generated_on')

@admin.register(AbsenteeismPrediction)
class AbsAdmin(admin.ModelAdmin):
    list_display = ('employee', 'risk_probability', 'risk_label', 'generated_on')
