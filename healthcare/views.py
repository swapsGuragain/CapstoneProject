from django.shortcuts import render
from .models import Patient
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm

def home(request):
	return render(request, 'home.html', {})

def tables(request):
	return render(request, 'tables.html', {})

def login_user(request):
	return render(request, 'login.html', {})
	# if request.user.is_authenticated:
	# 	return redirect('/')
	# if request.method == POST:
	# 	form = UserCreationForm(request.post)
	# else:
	# 	form = UserCreationForm()
	# 	return render(request, 'login.html', {'form' : form})


def logout_user(request):
	# return render(request, 'logout.html', {})
	pass