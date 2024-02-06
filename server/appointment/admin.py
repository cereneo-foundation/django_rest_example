from django.contrib import admin

from appointment.models import Appointment, Patient

admin.site.register(Appointment)
admin.site.register(Patient)