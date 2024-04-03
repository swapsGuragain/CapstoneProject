from django.db import models
from django.conf import settings

# One patient from Patients
class Patient(models.Model):
	user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, default = "", null = True)
	firstName = models.CharField(max_length = 50000)
	lastName = models.CharField(max_length = 50000)
	address = models.CharField(max_length = 50000, null = True)
	contact = models.CharField(max_length = 50000, null = True)
	dob = models.CharField(max_length = 50000, default="2023-01-01")
	gender = models.CharField(max_length = 20) 
	weight = models.DecimalField(decimal_places = 2, max_digits = 50)
	height = models.DecimalField(decimal_places = 2, max_digits = 50)
	healthHistory = models.CharField(max_length = 100000, default = '', blank = True, null = True)
	medication = models.CharField(max_length = 100000, default = '', blank = True, null = True)
	appointment = models.CharField(max_length = 100000, default = '', blank = True, null = True)
	key_value = models.CharField(max_length = 50000, default='', null = True)

	def __str__(self):
		return f"{self.firstName},{self.lastName},{self.dob},{self.gender},{self.weight},{self.height},{self.contact},{self.address},{self.medication},{self.appointment},{self.healthHistory}"

# Doctor from doctor's list
class Doctor(models.Model):
	user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, default = "", null = True)
	firstName = models.CharField(max_length = 500)
	lastName = models.CharField(max_length = 500)
	speciality = models.CharField(max_length = 500)
	phone = models.CharField(max_length = 500)
	key_value = models.CharField(max_length = 500, default='', null = True)

	def __str__(self):
		return f"{self.firstName}, {self.lastName},{self.speciality},{self.phone}"

class Appointment(models.Model):
	doctor = models.ForeignKey('Doctor', on_delete = models.CASCADE, related_name = 'leadsstatus')
	patient = models.ForeignKey('Patient', on_delete = models.CASCADE, related_name = 'leadsstatus')
	date = models.CharField(max_length = 500)
	time = models.CharField(max_length = 500)
	key_value = models.CharField(max_length = 500, default='', null = True)


	def __str__(self):
		return f"{self.doctor}, {self.patient},{self.date},{self.time}"

		


