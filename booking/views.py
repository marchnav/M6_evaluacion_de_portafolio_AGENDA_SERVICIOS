from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import BookingForm
from .models import Booking, Service, Slot


def service_list(request):
    services = Service.objects.filter(is_active=True).order_by("name")
    return render(request, "booking/service_list.html", {"services": services})


def service_detail(request, pk):
    service = get_object_or_404(Service, pk=pk, is_active=True)
    # próximos slots (hoy en adelante)
    now = timezone.now()
    upcoming_slots = service.slots.filter(start__gte=now).order_by("start")
    return render(
        request,
        "booking/service_detail.html",
        {"service": service, "upcoming_slots": upcoming_slots},
    )


def slot_list(request, service_id):
    service = get_object_or_404(Service, pk=service_id, is_active=True)
    now = timezone.now()
    slots = service.slots.filter(start__gte=now).order_by("start")
    return render(request, "booking/slot_list.html", {"service": service, "slots": slots})


@login_required
def booking_create(request, slot_id):
    slot = get_object_or_404(Slot, pk=slot_id)
    if request.method == "POST":
        form = BookingForm(request.POST, slot=slot, user=request.user)
        if form.is_valid():
            Booking.objects.create(
                slot=slot,
                user=request.user,
                notes=form.cleaned_data.get("notes", ""),
                status="PENDING",
            )
            messages.success(request, "Reserva creada. Estado: PENDIENTE.")
            return redirect("booking:my_bookings")
    else:
        form = BookingForm(slot=slot, user=request.user)

    return render(request, "booking/booking_form.html", {"form": form, "slot": slot})


@login_required
def my_bookings(request):
    bookings = (
        Booking.objects.filter(user=request.user)
        .select_related("slot__service")
        .order_by("-created_at")
    )
    return render(request, "booking/my_bookings.html", {"bookings": bookings})


def signup(request):
    """Autoregistro de usuarios con UserCreationForm."""
    if request.user.is_authenticated:
        return redirect("booking:service_list")

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # inicia sesión automáticamente
            messages.success(request, "Cuenta creada. ¡Bienvenido!")
            return redirect("booking:service_list")
    else:
        form = UserCreationForm()

    return render(request, "registration/signup.html", {"form": form})

def docs_why_django(request):
    """
    Página de investigación: por qué Django para aplicaciones empresariales,
    ventajas vs otros frameworks y cómo facilita desarrollo rápido y escalable.
    """
    return render(request, "docs/why_django.html")
