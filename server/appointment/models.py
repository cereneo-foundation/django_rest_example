from django.db import models


class Patient(models.Model):
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    birth_date = models.DateField()

    def __str__(self):
        return f'{self.first_name} {self.last_name} ({self.birth_date})'


class Appointment(models.Model):
    date = models.DateField()
    patient = models.ForeignKey(Patient, related_name="appointments", on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.date}: {self.patient.last_name}'
