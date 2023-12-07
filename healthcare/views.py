from django.shortcuts import render, redirect
from .models import Patient, User

from django.db import connections
import mysql.connector

from .ciph import getAge, getGender, getGenderBin, orderedWeight, orderedHeight, encrypt_pwd, wordEnc, wordDec, checkDups, decryptPatientData, decryptResultData
from cryptography.fernet import Fernet

from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm

from datetime import datetime

import pandas as pd

import csv
from django.http import HttpResponse



def home(request):
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

	# user = User.objects.all()

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
		return render(request, 'home.html', {'patients': patients})
	return render(request, 'home.html', {'patients': patients})

def patient(request, pk):

	cursor = connections['default'].cursor()
	queryCompleteness = 'SELECT * FROM patients WHERE id = %s;'	
	result = cursor.execute(queryCompleteness, pk)
	result = cursor.fetchall()


	result = decryptResultData(result[0])

	# print(result)

	# # check each details of the user in the both databse then only render else alert user

	# patient = Patient.objects.get(id = pk)

	# print(result, "//////////////", patient)

	return render(request, 'patient.html', {'patient': patient})

def tables(request):
	checkDups('Sourav', 'Thapa', 'muscle ache')
	return render(request, 'tables.html', {})

def login_user(request):
	if request.method == "POST":
		username =  request.POST['username']
		password = request.POST['password']

		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			messages.success(request, ("You have successuflly logged in!!"))
			return redirect('home')
		else:
			messages.success(request, ("There was an error while logging in!!"))
			return redirect('login')

	else:
		return render(request, 'login.html', {})

def logout_user(request):
	logout(request)
	messages.success(request, ("You have been logged out!!"))
	return redirect('login')

def addPatients(request):
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
		# dob = wordEnc(dob0, keyValue)
		dob = dob0
		healthHistory = wordEnc(healthHistory0, keyValue)

		checkDups(firstName0, lastName0, healthHistory0)


		cursor = connections['default'].cursor()
		queryDup = 'SELECT id FROM patients WHERE first_name = %s AND last_name = %s AND health_history = %s'	
		result = cursor.execute(queryDup, (firstName, lastName, healthHistory))
		if result:
			messages.success(request, ("User already exists!"))
			return redirect('home')

		newPatient = Patient(firstName = firstName.decode(), lastName = lastName.decode(), dob = dob, gender = gender, weight = weight, height = height, healthHistory = healthHistory.decode())
		newPatient.save()

		query1 = 'INSERT INTO patients (first_name, last_name, dob, gender, weight, height, health_history, keyValues) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);'
		cursor.execute(query1, [firstName, lastName, dob, gender, weight, height, healthHistory, keyValue])
		
		messages.success(request, ("successuflly added new Patient "+firstName0))
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


