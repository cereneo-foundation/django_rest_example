from rest_framework import serializers
from appointment.models import Patient, Appointment


class PatientSerializer(serializers.HyperlinkedModelSerializer):
    appointments = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='appointment-detail'
    )

    class Meta:
        model = Patient
        fields = ['url', 'first_name', 'last_name', 'birth_date', 'appointments']


class AppointmentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Appointment
        fields = ['url', 'date', 'patient']