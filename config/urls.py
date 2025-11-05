from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('booking.urls')),  # rutas públicas de la app
    path('accounts/', include('django.contrib.auth.urls')),  # login/logout/password views
]
