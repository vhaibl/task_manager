from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models

# Create your models here.
from django.utils import timezone


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
    planned_by = models.DateTimeField(validators=[MinValueValidator(limit_value=timezone.now())])
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title + ', ' + self.status + ', ' + self.created.strftime('%Y-%m-%d %H:%M') + ' - ' + self.planned_by.strftime(
            '%Y-%m-%d %H:%M') + ', ' + self.author.first_name + " " + self.author.last_name
