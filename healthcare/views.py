from django.shortcuts import render, redirect
from .models import Patient
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm

def home(request):
	return render(request, 'home.html', {})

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
	return render(request, 'addPatients.html', {})


