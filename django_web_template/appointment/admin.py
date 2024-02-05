from django.contrib import admin

from django_web_template.appointment.models import Appointment, Patient

# Register your models here.
admin.site.register(Appointment)
admin.site.register(Patient)
