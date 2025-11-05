from django.urls import path
from . import views

app_name = "booking"

urlpatterns = [
    path("", views.service_list, name="service_list"),
    path("servicio/<int:pk>/", views.service_detail, name="service_detail"),
    path("servicio/<int:service_id>/slots/", views.slot_list, name="slot_list"),
    path("reservar/<int:slot_id>/", views.booking_create, name="booking_create"),
    path("mis-reservas/", views.my_bookings, name="my_bookings"),
    path("signup/", views.signup, name="signup"),

]
