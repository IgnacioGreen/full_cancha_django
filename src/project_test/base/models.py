from django.db import models
from django.contrib.auth.models import User


class Event(models.Model):
    title = models.CharField(max_length=255)
    start = models.DateTimeField()
    end = models.DateTimeField()
    color = models.CharField(max_length=9, default="#FFFFFF")  # Color en formato hexadecimal (#FFFFFF)
    allDay = models.BooleanField(default=False)  # Indica si el evento dura todo el día
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='created_events', null=True, blank=True)
    modified_by = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='modified_events', null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)  # Se establece cuando se crea el evento
    modified = models.DateTimeField(auto_now=True)     # Se actualiza cada vez que se guarda el evento

    def __str__(self):
        return f"{self.title} ({self.start} - {self.end})"
