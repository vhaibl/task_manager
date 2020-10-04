from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone

from simple_history.models import HistoricalRecords


class Task(models.Model):
    status_choices = (
        ('NEW', 'New'),
        ('PLANNED', 'Planned'),
        ('INPROGRESS', 'In progress'),
        ('COMPLETED', 'Completed'),
    )
    title = models.CharField(max_length=120)
    description = models.TextField(max_length=1024)
    status = models.CharField(max_length=15, choices=status_choices)
    planned_by = models.DateTimeField(validators=[MinValueValidator(limit_value=timezone.now())], blank=True, null=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    history = HistoricalRecords()

    def __str__(self):
        return self.title + ', ' + self.status + ', ' + self.author.first_name + " " + self.author.last_name
