from django.db import models

from django.db import models

class Employee(models.Model):
    name = models.CharField(max_length=100)
    department = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class DailyReport(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    date = models.DateField()

    inbound = models.PositiveIntegerField(null=True, blank=True, default=None)
    outbound = models.PositiveIntegerField(null=True, blank=True, default=None)
    shipment = models.PositiveIntegerField(null=True, blank=True, default=None)
    customs = models.PositiveIntegerField(null=True, blank=True, default=None)
    delivery = models.PositiveIntegerField(null=True, blank=True, default=None)
    special_tag = models.PositiveIntegerField(null=True, blank=True, default=None)

    remarks = models.TextField(blank=True, null=True)
    canceled = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('employee', 'date')
        ordering = ['-date']

    def __str__(self):
        return f"{self.employee.name} - {self.date}"

