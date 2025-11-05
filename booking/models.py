from django.conf import settings
from django.db import models

class Service(models.Model):
    name = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Slot(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name="slots")
    start = models.DateTimeField()
    end = models.DateTimeField()
    capacity = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ["start"]
        constraints = [
            models.CheckConstraint(check=models.Q(end__gt=models.F("start")), name="slot_end_after_start"),
            models.CheckConstraint(check=models.Q(capacity__gte=1), name="slot_capacity_min1"),
        ]

    def __str__(self):
        return f"{self.service.name} — {self.start:%Y-%m-%d %H:%M} → {self.end:%H:%M}"


class Booking(models.Model):
    STATUS_CHOICES = [
        ("PENDING", "Pendiente"),
        ("CONFIRMED", "Confirmada"),
        ("CANCELLED", "Cancelada"),
    ]

    slot = models.ForeignKey(Slot, on_delete=models.CASCADE, related_name="bookings")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="bookings")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="PENDING")
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("slot", "user")  # evita doble reserva del mismo usuario en el mismo slot
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user} → {self.slot} [{self.status}]"
