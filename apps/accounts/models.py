from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_ADMIN = 'admin'
    ROLE_EMPLOYEE = 'employee'
    ROLES = [(ROLE_ADMIN, 'Admin'), (ROLE_EMPLOYEE, 'Employee')]

    role = models.CharField(max_length=10, choices=ROLES, default=ROLE_EMPLOYEE)

    def is_admin(self):
        return self.role == self.ROLE_ADMIN

    def __str__(self):
        return f"{self.get_full_name() or self.username} ({self.role})"
