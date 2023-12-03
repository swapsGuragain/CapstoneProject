from django.shortcuts import render, redirect
from .models import Patient
from .ciph import getAge, getGender, getGenderBin
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from datetime import datetime

def home(request):

	patients = Patient.objects.all()
	print(patients[1])

	return render(request, 'home.html', {'patients': patients})

def tables(request):
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
	return redirect('home')

def addPatients(request):
	if request.method == "POST":
		firstName = request.POST.get('firstname')
		lastName = request.POST.get('lastname')
		age = getAge(request.POST.get('dob'))
		gender = getGenderBin(request.POST.get('gender'))
		weight = request.POST.get('weight')
		height = request.POST.get('height')
		healthHistory = request.POST.get('helhis')

		newPatient = Patient(firstName = firstName, lastName = lastName, age = age, gender = gender, weight = weight, height = height, healthHistory = healthHistory)
		newPatient.save()

	return render(request, 'addPatients.html', {})


