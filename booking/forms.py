from django import forms
from django.core.exceptions import ValidationError
from .models import Booking

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ["notes"]  # status lo maneja la app; slot y user se setean en la vista

    def __init__(self, *args, **kwargs):
        # slot y user llegan por kwargs para validar
        self.slot = kwargs.pop("slot", None)
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned = super().clean()
        if not self.slot or not self.user:
            raise ValidationError("Faltan datos de contexto para crear la reserva.")

        # Evitar doble reserva del mismo usuario en el mismo slot (además del unique_together)
        if Booking.objects.filter(slot=self.slot, user=self.user).exclude(status="CANCELLED").exists():
            raise ValidationError("Ya tienes una reserva para este horario.")

        # Validar capacidad: contamos reservas no canceladas
        current_count = Booking.objects.filter(slot=self.slot).exclude(status="CANCELLED").count()
        if current_count >= self.slot.capacity:
            raise ValidationError("No quedan cupos disponibles para este horario.")

        return cleaned
