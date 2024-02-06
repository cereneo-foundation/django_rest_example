from rest_framework import viewsets

from appointment.models import Patient, Appointment
from appointment.serializers import PatientSerializer, AppointmentSerializer


class PatientViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows patients to be viewed or edited.
    """
    model = Patient
    queryset = Patient.objects.all().order_by('last_name', 'first_name')
    serializer_class = PatientSerializer


class AppointmentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows patients to be viewed or edited.
    """
    model = Appointment
    queryset = Appointment.objects.all().order_by('date')
    serializer_class = AppointmentSerializer