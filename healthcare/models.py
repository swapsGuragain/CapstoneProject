from django.db import models
import datetime


# Patients
# class PatientList(models.Model):
# 	firstName = models.CharField(max_length = 50)
# 	lastName = models.CharField(max_length = 50)
# 	age =
# 	gender = models.CharField(max_length = 50)
# 	weight = models.DecimalField(decimal_places = 2, max_digits = 5)
# 	height = models.DecimalField(decimal_places = 2, max_digits = 5)
# 	healthHistory = models.CharField(max_length = 500, default = '', blank = True, null = True)


# 	def __str__(self):
# 		return f'{self.firstName} {self.lastName} {self.age} {self.gender} {self.weight} {self.height} {self.healthHistory}'


# One patient from Patients
class Patient(models.Model):
	firstName = models.CharField(max_length = 500)
	lastName = models.CharField(max_length = 500)
	dob = models.CharField(max_length = 500, default="2023-01-01")
	gender = models.CharField(max_length = 10) 
	weight = models.DecimalField(decimal_places = 2, max_digits = 50)
	height = models.DecimalField(decimal_places = 2, max_digits = 50)
	healthHistory = models.CharField(max_length = 1000, default = '', blank = True, null = True)

	def __str__(self):

		return f"{self.firstName},{self.lastName},{self.dob},{self.gender},{self.weight},{self.height},{self.healthHistory}"




class User(models.Model):

	name = models.CharField(max_length = 50)
	password = models.CharField(max_length = 10000)
	email = models.EmailField(max_length=100)
	isAuthenticated = models.BooleanField(default = False)
	isHealthWorker = models.BooleanField(default = False)
	isResearcher = models.BooleanField(default = False)


	def __str__(self):
		return self.name

		


