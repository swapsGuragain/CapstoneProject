from django.shortcuts import render, redirect
from .models import Patient, User

from django.db import connections
import mysql.connector

from .ciph import getAge, getGender, getGenderBin, orderedWeight, orderedHeight, encrypt_pwd

from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm

from datetime import datetime

import csv
from django.http import HttpResponse

authenticateUser = False

def home(request):

	if request.method == 'FETCH':
		response = HttpResponse(content_type="text/csv")

		writer = csv.writer(response)
		writer.writerow(["Age", "Gender", "Weight", "Height", "Health_history"])

		for patient in Patient.objects.all().values_list('age', 'gender', 'weight', 'height', 'healthHistory'):
			writer.writerow(patient)

		response['Content-Disposition'] = 'attachment; filename="patients.csv"'
		return response

	# check the counts from both database and compare then only render else alert user

	patients = Patient.objects.all()



	return render(request, 'home.html', {'patients': patients})

def patient(request, pk):

	# check each details of the user in the both databse then only render else alert user

	patient = Patient.objects.get(id = pk)
	print(patient)

	return render(request, 'patient.html', {'patient': patient})


def tables(request):
	return render(request, 'tables.html', {})

def login_user(request):
	if request.method == "POST":
		username =  request.POST['username']
		password = encrypt_pwd(request.POST['password'])

		authenticateUser = True

		# user = authenticate(request, username=username, password=password)
		# if user is not None:
		# 	login(request, user)
		# 	messages.success(request, ("You have successuflly logged in!!"))
		# 	return redirect('home')
		# else:
		# 	messages.success(request, ("There was an error while logging in!!"))
		# 	return redirect('login')
	else:
		return render(request, 'login.html', {'authenticateUser': authenticateUser})


def logout_user(request):
	authenticateUser = False
	logout(request)
	messages.success(request, ("You have been logged out!!"))
	return redirect('home')

def addPatients(request):
	if request.method == "POST":
		firstName = request.POST.get('firstname')
		lastName = request.POST.get('lastname')
		age = getAge(request.POST.get('dob'))
		gender = getGenderBin(request.POST.get('gender'))
		weight = orderedWeight(request.POST.get('weight'))
		height = orderedHeight(request.POST.get('height'))
		healthHistory = request.POST.get('helhis')

		cursor = connections['default'].cursor()
		queryDup = 'SELECT id FROM patients WHERE first_name = %s AND last_name = %s AND health_history = %s'	
		result = cursor.execute(queryDup, (firstName, lastName, healthHistory))
		if result:
			messages.success(request, ("User already exists!"))
			return redirect('home')

		newPatient = Patient(firstName = firstName, lastName = lastName, age = age, gender = gender, weight = weight, height = height, healthHistory = healthHistory)
		newPatient.save()

		query1 = 'INSERT INTO patients (first_name, last_name, age, gender, weight, height, health_history) VALUES (%s, %s, %s, %s, %s, %s, %s);'
		cursor.execute(query1, [firstName, lastName, age, gender, weight, height, healthHistory])
		
		messages.success(request, ("successuflly added new Patient"+firstName))
		# return redirect('patient', id)
		return redirect('home')

	return render(request, 'addPatients.html', {})

def addUser(request):
	if request.method == "POST":
		name = request.POST.get('name')
		password = encrypt_pwd(request.POST.get('password'))
		email = request.POST.get('email')
		isHealthWorker = request.POST.get('healthWorker')
		if isHealthWorker == 'H':
			isHealthWorker = 1
		else:
			isHealthWorker = 0
		isResearcher = request.POST.get('researcher')
		if isResearcher == 'R':
			isResearcher = 1
		else:
			isResearcher = 0

		newUser = User(name = name, password = password, email = email, isHealthWorker = isHealthWorker, isResearcher = isResearcher)
		newUser.save()

		return redirect('home')

	return render(request, 'addUser.html', {})


