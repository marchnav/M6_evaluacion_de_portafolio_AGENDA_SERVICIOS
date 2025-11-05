Agenda de Servicios — Django (README)

Aplicación web en Django 5 para administrar un catálogo de servicios, crear bloques horarios (slots) y permitir que usuarios autenticados realicen reservas con control de cupos. Incluye panel Django Admin para gestionar Servicios, Slots y Reservas, y autoregistro de usuarios.

------------------------------------------------------------
Requisitos
- Python 3.11+ (probado con 3.13)
- pip

------------------------------------------------------------
Instalación rápida
1) Crear y activar entorno virtual
   python -m venv .venv
   (Windows PowerShell) .\.venv\Scripts\Activate

2) Instalar dependencias
   pip install "Django>=5.0,<6.0"

3) Migraciones
   python manage.py makemigrations
   python manage.py migrate

4) Crear superusuario (para /admin)
   python manage.py createsuperuser

5) Ejecutar servidor
   python manage.py runserver

------------------------------------------------------------
Estructura principal

config/                # proyecto (settings, urls, wsgi)
booking/               # app principal
  - models.py          # Service, Slot, Booking
  - views.py           # vistas públicas + signup
  - urls.py            # rutas namespaced (booking)
  - forms.py           # BookingForm (validaciones)
  - admin.py           # admin personalizado
templates/
  - base.html
  - booking/
      - service_list.html
      - service_detail.html
      - slot_list.html
      - booking_form.html
      - my_bookings.html
  - registration/
      - login.html
      - signup.html

------------------------------------------------------------
Modelos

Service:
- name, description, price, is_active

Slot:
- service(FK), start, end, capacity
- Reglas: end > start, capacity ≥ 1

Booking:
- slot(FK), user(FK), status [PENDING|CONFIRMED|CANCELLED], notes, created_at
- Restricción: única por (slot, user) para evitar doble reserva

------------------------------------------------------------
Rutas principales

/                         -> Lista de servicios
/servicio/<id>/           -> Detalle del servicio + próximos slots
/servicio/<id>/slots/     -> Lista de slots del servicio
/reservar/<slot_id>/      -> Formulario de reserva (requiere login)
/mis-reservas/            -> Reservas del usuario (requiere login)
/signup/                  -> Crear cuenta (autoregistro)
/accounts/login/          -> Login
/accounts/logout/         -> Logout

Redirecciones configuradas en settings.py:
- LOGIN_REDIRECT_URL = '/'
- LOGOUT_REDIRECT_URL = '/'

------------------------------------------------------------
Flujo de uso

1. Ingresar a /admin con el superusuario.
2. Crear un Service.
3. Crear uno o más Slot futuros para ese servicio (capacity ≥ 1).
4. (Usuario) Registrarse en /signup/ o iniciar sesión en /accounts/login/.
5. Elegir servicio -> horario -> Reservar.
6. Ver “Mis reservas” en /mis-reservas/.

------------------------------------------------------------
Permisos y roles

- Usuarios autenticados: pueden reservar y ver sus reservas.
- Staff/Admin: gestionan Servicios, Slots y Reservas en Django Admin
  (acciones masivas: Confirmar / Cancelar; filtros por estado, servicio y fecha).

------------------------------------------------------------
Notas técnicas

- Templates centralizados: DIRS = [BASE_DIR / 'templates']
- BookingForm valida:
  - Doble reserva del mismo usuario en el mismo slot (y se refuerza con unique_together).
  - No exceder la capacidad (cuenta reservas no canceladas).
- Estilo simple y responsive (CSS en base.html).
- Recomendado para producción: crear requirements.txt con:
  Django>=5.0,<6.0

------------------------------------------------------------
Licencia
Uso educativo/portafolio.
