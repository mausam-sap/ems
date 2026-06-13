from django.db import models
from apps.employees.models import Employee
from apps.accounts.models import User

class LeaveRequest(models.Model):
    TYPE_ANNUAL = 'Annual'
    TYPE_SICK = 'Sick'
    TYPE_CASUAL = 'Casual'
    LEAVE_TYPES = [(TYPE_ANNUAL, 'Annual'), (TYPE_SICK, 'Sick'), (TYPE_CASUAL, 'Casual')]

    STATUS_PENDING = 'Pending'
    STATUS_APPROVED = 'Approved'
    STATUS_REJECTED = 'Rejected'
    STATUS_CHOICES = [
        (STATUS_PENDING, 'Pending'),
        (STATUS_APPROVED, 'Approved'),
        (STATUS_REJECTED, 'Rejected'),
    ]

    ANNUAL_LIMIT = 12
    SICK_LIMIT = 6
    CASUAL_LIMIT = 6

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='leave_requests')
    leave_type = models.CharField(max_length=10, choices=LEAVE_TYPES)
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=STATUS_PENDING)
    applied_on = models.DateTimeField(auto_now_add=True)
    reviewed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    review_note = models.TextField(blank=True)

    @property
    def days_count(self):
        return (self.end_date - self.start_date).days + 1

    def __str__(self):
        return f"{self.employee} - {self.leave_type} ({self.start_date} to {self.end_date})"
