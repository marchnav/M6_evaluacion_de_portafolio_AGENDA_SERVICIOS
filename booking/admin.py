from django.contrib import admin
from .models import Service, Slot, Booking

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "is_active")
    list_filter = ("is_active",)
    search_fields = ("name", "description")


@admin.register(Slot)
class SlotAdmin(admin.ModelAdmin):
    list_display = ("service", "start", "end", "capacity")
    list_filter = ("service", "start")
    search_fields = ("service__name",)
    date_hierarchy = "start"


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("slot", "user", "status", "created_at")
    list_filter = ("status", "slot__service", "slot__start")
    search_fields = ("user__username", "user__email", "slot__service__name", "notes")
    actions = ["mark_confirmed", "mark_cancelled"]

    @admin.action(description="Marcar seleccionadas como CONFIRMADAS")
    def mark_confirmed(self, request, queryset):
        queryset.update(status="CONFIRMED")

    @admin.action(description="Marcar seleccionadas como CANCELADAS")
    def mark_cancelled(self, request, queryset):
        queryset.update(status="CANCELLED")
