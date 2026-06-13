from django import forms
from apps.employees.models import Employee
import datetime

MONTH_CHOICES = [(i, datetime.date(2000, i, 1).strftime('%B')) for i in range(1, 13)]
YEAR_CHOICES = [(y, y) for y in range(datetime.date.today().year - 2, datetime.date.today().year + 1)]

class GeneratePayrollForm(forms.Form):
    employee = forms.ModelChoiceField(
        queryset=Employee.objects.filter(is_active=True),
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    month = forms.ChoiceField(choices=MONTH_CHOICES, widget=forms.Select(attrs={'class': 'form-select'}))
    year = forms.ChoiceField(choices=YEAR_CHOICES, widget=forms.Select(attrs={'class': 'form-select'}))
    bonus = forms.DecimalField(
        initial=0, min_value=0,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
