from rest_framework import viewsets

from django_web_template.appointment.models import Patient, Appointment
from django_web_template.appointment.serializers import PatientSerializer, AppointmentSerializer
from django_web_template.jwt_extension.logger import LoggingMixin


class PatientViewSet(LoggingMixin, viewsets.ModelViewSet):
    """
    API endpoint that allows patients to be viewed or edited.
    """
    model = Patient
    queryset = Patient.objects.all().order_by('last_name', 'first_name')
    serializer_class = PatientSerializer


class AppointmentViewSet(LoggingMixin, viewsets.ModelViewSet):
    """
    API endpoint that allows patients to be viewed or edited.
    """
    queryset = Appointment.objects.all().order_by('date')
    serializer_class = AppointmentSerializer
