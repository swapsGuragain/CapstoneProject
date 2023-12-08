from django.shortcuts import render, redirect
from .models import Patient, User

from django.db import connections
import mysql.connector

from .ciph import getAge, getGender, getGenderBin, orderedWeight, orderedHeight, encrypt_pwd, wordEnc, checkDups, decryptPatientData, decryptResultData, decryptPatient
from cryptography.fernet import Fernet

from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm

from datetime import datetime

import pandas as pd

import csv
from django.http import HttpResponse

authenticatedUser = False
isH = False
isR = False

def home(request):
	global authenticatedUser, isH, isR
	if not request.user.is_authenticated:
		messages.success(request, ('You need to login first!'))
		return redirect('login')

	if request.method == 'POST':
		weight01 = orderedWeight(request.POST.get('startWeight'))
		weight02 = orderedWeight(request.POST.get('endWeight'))

		cursor = connections['default'].cursor()
		qKeyVal = 'SELECT keyValues FROM patients WHERE weight between %s and %s;'	
		keyVal = cursor.execute(qKeyVal, [weight01, weight02])
		keyVal = cursor.fetchall()

		patients = Patient.objects.filter(weight__range=(weight01, weight02))

		i = 0
		for patient in patients:
			patient = decryptPatientData(patient, keyVal[i])
			patient.age = getAge(patient.dob)
			i = i+1

		return render(request, 'home.html', {'patients': patients, 'isHealthWorker': isH, 'isResearcher': isR})

	if request.method == 'FETCH':
		response = HttpResponse(content_type="text/csv")
		writer = csv.writer(response)
		writer.writerow(["Dob", "Gender", "Weight", "Height", "Health_history"])
		for patient in Patient.objects.all().values_list('dob', 'gender', 'weight', 'height', 'healthHistory'):
			writer.writerow(patient)
		response['Content-Disposition'] = 'attachment; filename="patients.csv"'
		return response
	cursor = connections['default'].cursor()
	queryCompleteness = 'SELECT COUNT(*) FROM patients;'	
	result = cursor.execute(queryCompleteness)
	result = cursor.fetchall()

	queryCompleteness = 'SELECT keyValues FROM patients;'	
	keyVal = cursor.execute(queryCompleteness)
	keyVal = cursor.fetchall()

	patients = Patient.objects.all()

	i = 0
	for patient in patients:
		patient = decryptPatientData(patient, keyVal[i])
		patient.age = getAge(patient.dob)
		i = i+1

	if result[0][0] > patients.count():
		messages.success(request, ("There has been some type of alteration in the cloud database. The query result is incomplete. Some data items from the database are missing."))
	elif result[0][0] < patients.count():
		messages.success(request, ("There has been alteration in cloud database. The query result is overfitted. Some dataitems may have duplicates."))
	else:
		return render(request, 'home.html', {'patients': patients, 'isHealthWorker': isH, 'isResearcher': isR})
	
	return render(request, 'home.html', {'patients': patients, 'isHealthWorker': isH, 'isResearcher': isR})

def patient(request, pk):
	global authenticatedUser, isH, isR
	if not request.user.is_authenticated:
		messages.success(request, ('You need to login first!'))
		return redirect('login')
	if isH != True:
		messages.success(request, ('You have no access to add new patients!'))
		return redirect('home')
	cursor = connections['default'].cursor()
	queryCompleteness = 'SELECT * FROM patients WHERE id = %s;'	
	result = cursor.execute(queryCompleteness, pk)
	result = cursor.fetchall()

	result = decryptResultData(result[0])

	# # check each details of the user in the both databse then only render else alert user

	patient = Patient.objects.get(id = pk)
	patient = decryptPatient(patient, result[7])
	patient.age = getAge(patient.dob)

	if result[0] != patient.firstName:
		messages.success(request, ('first name has been changed'))
	elif result[1] != patient.lastName:
		messages.success(request, ('last name has been changed'))
	elif result[2] != patient.gender:
		messages.success(request, ('gender data has been changed'))

	elif result[3] != patient.weight:
		messages.success(request, ('weight data has been changed'))

	elif result[4] != patient.height:
		messages.success(request, ('height data has been changed'))

	elif result[5] != patient.healthHistory:
		messages.success(request, ('Health history has been changed'))

	elif result[6] != patient.dob:
		messages.success(request, ('date of birth has been changed'))
	else:
		messages.success(request, ('Patient found!'))

	return render(request, 'patient.html', {'patient': patient, 'isHealthWorker': isH, 'isResearcher': isR})

def tables(request):
	global authenticatedUser, isH, isR
	if not request.user.is_authenticated:
		messages.success(request, ('You need to login first!'))
		return redirect('login')
	if isR != True:
		messages.success(request, ('You have no access to table data!'))
		return redirect('home')
	checkDups('Sourav', 'Thapa', 'muscle ache')
	return render(request, 'tables.html', {'isHealthWorker': isH, 'isResearcher': isR})

def login_user(request):
	global authenticatedUser, isH, isR
	if request.method == "POST":
		username =  request.POST['username']
		password = request.POST['password']

		user = authenticate(request, username=username, password=password)

		cursor = connections['default'].cursor()
		queryUser = 'SELECT * FROM healthcare_user WHERE name = %s;'	
		uSer = cursor.execute(queryUser, username)
		uSer = cursor.fetchall()

		if uSer[0][4] == 1:
			global isH 
			isH = True 

		if uSer[0][5] == 1:
			global isR
			isR = True 

		if user is not None:
			login(request, user)
			messages.success(request, ("You have successuflly logged in!!"))
			authenticatedUser = True
			return redirect('home')
		else:
			messages.success(request, ("There was an error while logging in!!"))
			return redirect('login')

	else:
		return render(request, 'login.html', {'isHealthWorker': isH, 'isResearcher': isR})

def logout_user(request):
	logout(request)
	global authenticatedUser, isH, isR
	authenticatedUser = False
	isH = False
	isR = False
	messages.success(request, ("You have been logged out!!"))
	return redirect('login')

def addPatients(request):
	global authenticatedUser, isH, isR
	if not request.user.is_authenticated:
		messages.success(request, ('You need to login first!'))
		return redirect('login')
	if isH != True:
		messages.success(request, ('You have no access to add new patients!'))
		return redirect('home')
	if request.method == "POST":
		firstName0 = request.POST.get('firstname')
		lastName0 = request.POST.get('lastname')
		dob0 = request.POST.get('dob')
		age = getAge(dob0)
		gender = getGenderBin(request.POST.get('gender'))
		weight = orderedWeight(request.POST.get('weight'))
		height = orderedHeight(request.POST.get('height'))
		healthHistory0 = request.POST.get('helhis')
		keyValue = Fernet.generate_key()
		firstName = wordEnc(firstName0, keyValue)
		lastName = wordEnc(lastName0, keyValue)
		dob = wordEnc(dob0, keyValue)
		healthHistory = wordEnc(healthHistory0, keyValue)

		cursor = connections['default'].cursor()

		if checkDups(firstName0, lastName0):
			messages.success(request, ("User already exists!"))
			return redirect('home')

		newPatient = Patient(firstName = firstName.decode(), lastName = lastName.decode(), dob = dob.decode(), gender = gender, weight = weight, height = height, healthHistory = healthHistory.decode())
		newPatient.save()

		query1 = 'INSERT INTO patients (first_name, last_name, dob, gender, weight, height, health_history, keyValues) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);'
		cursor.execute(query1, [firstName, lastName, dob, gender, weight, height, healthHistory, keyValue])
		
		messages.success(request, ("successuflly added new Patient "+firstName0))
		return redirect('home')

	return render(request, 'addPatients.html', {'isHealthWorker': isH, 'isResearcher': isR})

def addUser(request):
	global authenticatedUser, isH, isR
	if not request.user.is_authenticated:
		messages.success(request, ('You need to login first!'))
		return redirect('login')
	if isH != True:
		messages.success(request, ('You have no access to add new patients!'))
		return redirect('home')
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

	return render(request, 'addUser.html', {'isHealthWorker': isH, 'isResearcher': isR})


