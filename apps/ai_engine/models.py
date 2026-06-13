from django.db import models
from apps.employees.models import Employee

class PerformancePrediction(models.Model):
    RISK_LOW = 'Low'
    RISK_MEDIUM = 'Medium'
    RISK_HIGH = 'High'
    RISK_CHOICES = [(RISK_LOW, 'Low'), (RISK_MEDIUM, 'Medium'), (RISK_HIGH, 'High')]

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='performance_predictions')
    predicted_score = models.FloatField()
    risk_label = models.CharField(max_length=10, choices=RISK_CHOICES)
    attendance_rate = models.FloatField()
    generated_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-generated_on']

    def __str__(self):
        return f"{self.employee} - Score: {self.predicted_score:.1f} ({self.risk_label})"

class AbsenteeismPrediction(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='absenteeism_predictions')
    risk_probability = models.FloatField()
    risk_label = models.CharField(max_length=10)
    generated_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-generated_on']

    def __str__(self):
        return f"{self.employee} - Absenteeism Risk: {self.risk_label}"
