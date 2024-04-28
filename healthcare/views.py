from django.shortcuts import render, redirect
from .models import Patient, Doctor, Appointment
from .ciph import wordEnc, orderedNumber, getGenderBin, decryptDoctor, decryptPatient, decryptAppointment

from cryptography.fernet import Fernet

from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group, User
from django.contrib.auth.decorators import login_required, user_passes_test

from datetime import datetime

# Check the group for user
def has_group(user, group):
    return user.groups.filter(name=group).exists()
def is_admin(user):
    return user.is_staff
def is_doctor(user):
    return user.groups.filter(name='doctor').exists()
def is_patient(user):
    return user.groups.filter(name='patient').exists()

# View for everyone

def home(request):
	return render(request, 'home.html')

def login_user(request):
	error = ""
	if request.method == "POST":
		u =  request.POST['username']
		p = request.POST['password']
		user = authenticate(username=u, password=p)
		try:
			if user.is_authenticated:
				login(request, user)
				error = "no"
			else:
				error = "yes"
		except:
			error = "yes"
	d = {'error': error}
	return render(request, 'login.html', d)

def tables(request):
	if not request.user.is_authenticated:
		messages.success(request, ('You need to login first!'))
		return redirect('login')
	return render(request, 'tables.html', {})

def	contact(request):
	return render(request, 'contact.html', {})

def	about(request):
	return render(request, 'about.html', {})

def guestRegister_patient(request):
	if request.method == "POST":
		form = UserCreationForm(request.POST)
		if form.is_valid():
			user = form.save()
			user.save()
			user_group = Group.objects.get(name='patient') 
			user.groups.add(user_group)
			login(request, user)
			messages.success(request, user.id)
			return redirect('guestAddPatient', user.id)
	else:
		form = UserCreationForm()
	return render(request, 'guestRegister_patient.html', {'form':form})

def logout_user(request):
	if not request.user.is_authenticated:
		return redirect('login')
	logout(request)
	return redirect('login')

# View for admin

@login_required(login_url='login')
@user_passes_test(is_admin)
def	index(request):
	if not request.user.is_staff:
		redirect('login')
	doc = Doctor.objects.all()
	patients = Patient.objects.all()
	appoint = Appointment.objects.all()
	# decrypt doc
	for do in doc:
		do = decryptDoctor(do)
	# decrypt patient
	for pa in patients:
		pa = decryptPatient(pa)
	# decrypt appoinntment
	for ap in appoint:
		ap = decryptAppointment(ap)
	d = {'d':doc.count(), 'p':patients.count(), 'a':appoint.count()}
	return render(request, 'index.html', d)

# Admin - patient views

@login_required(login_url='login')
@user_passes_test(is_admin)
def register_user(request):
	if request.method == "POST":
		form = UserCreationForm(request.POST)
		if form.is_valid():
			user = form.save()
			user.save()
			user_group = Group.objects.get(name='patient') 
			user.groups.add(user_group)
			messages.success(request, user.id)
			print("register_user", user.id)
			return redirect('addPatient_pk', user.id)
	else:
		form = UserCreationForm()
	return render(request, 'register.html', {'form':form})

@login_required(login_url='login')
@user_passes_test(is_admin)
def register_doc(request):
	if request.method == 'POST':
		form = UserCreationForm(request.POST)
		if form.is_valid():
			user = form.save()
			user.save()
			user_group = Group.objects.get(name='doctor') 
			user.groups.add(user_group)
			return redirect('addDoctor_pk', user.id)
	else:
		form = UserCreationForm()
	return render(request, 'register_doc.html', {'form':form})

@login_required(login_url='login')
@user_passes_test(is_admin)
def addPatient_pk(request, pk):
	error = ""
	if not request.user.is_authenticated:
		return redirect('login')
	if request.method == "POST":
		fName = request.POST.get('fName')
		lName = request.POST.get('lName')
		address = request.POST.get('address')
		contact = request.POST.get('contact')
		dob = request.POST.get('dob')
		gender = request.POST.get('gender')
		weight = request.POST.get('weight')
		height = request.POST.get('height')
		healthHistory = request.POST.get('helhis')
		medication = request.POST.get('medication')
		patient01 = User.objects.get(id=pk)
		# encrypt patient data here 
		key_value = Fernet.generate_key()
		fName = wordEnc(fName, key_value).decode()
		lName = wordEnc(lName, key_value).decode()
		address = wordEnc(address, key_value).decode()
		contact = wordEnc(contact, key_value).decode()
		dob = wordEnc(dob, key_value).decode()
		healthHistory = wordEnc(healthHistory, key_value).decode()
		medication = wordEnc(medication, key_value).decode()
		weight = orderedNumber(weight)
		height = orderedNumber(height)
		gender = getGenderBin(gender)
		key_value = key_value.decode()
		try:
			Patient.objects.create(user = patient01, firstName = fName, lastName = lName, address = address, contact = contact, dob = dob, gender = gender, weight = weight, height = height, healthHistory = healthHistory, medication = medication, key_value = key_value)
			error = "no"
		except:
			error = "yes"
	d = {'error':error, 'id': pk}
	return render(request, 'addPatient_pk.html', d)

@login_required(login_url='login')
@user_passes_test(is_admin)
def addPatient(request):
	error = ""
	if not request.user.is_authenticated:
		return redirect('login')
	if request.method == "POST":
		fName = request.POST.get('fName')
		lName = request.POST.get('lName')
		address = request.POST.get('address')
		contact = request.POST.get('contact')
		dob = request.POST.get('dob')
		gender = request.POST.get('gender')
		weight = request.POST.get('weight')
		height = request.POST.get('height')
		healthHistory = request.POST.get('helhis')
		medication = request.POST.get('medication')
		appointment = request.POST.get('appointment')
		# patientId = request.POST.get('patient')
		# patient01 = User.objects.get(id=patientId)
		# encrypt patient data here 
		key_value = Fernet.generate_key()
		fName = wordEnc(fName, key_value).decode()
		lName = wordEnc(lName, key_value).decode()
		address = wordEnc(address, key_value).decode()
		contact = wordEnc(contact, key_value).decode()
		dob = wordEnc(dob, key_value).decode()
		healthHistory = wordEnc(healthHistory, key_value).decode()
		medication = wordEnc(medication, key_value).decode()
		weight = orderedNumber(weight)
		height = orderedNumber(height)
		gender = getGenderBin(gender)
		key_value = key_value.decode()
		try:
			Patient.objects.create( firstName = fName, lastName = lName, address = address, contact = contact, dob = dob, gender = gender, weight = weight, height = height, healthHistory = healthHistory, medication = medication, key_value = key_value)
			error = "no"
		except:
			error = "yes"
	d = {'error':error}
	return render(request, 'addPatient.html', d)

@login_required(login_url='login')
@user_passes_test(is_admin)
def patientsList(request):
	if not request.user.is_authenticated:
		return redirect('login')
	patients = Patient.objects.all()
	# decrypt patient 
	for pa in patients:
		pa = decryptPatient(pa)
	d = {'patients': patients}
	return render(request, 'patientsList.html', d)

@login_required(login_url='login')
@user_passes_test(is_admin)
def patient(request, pk):
	if not request.user.is_authenticated:
		messages.success(request, ('You need to login first!'))
		return redirect('login')
	patient = Patient.objects.get(id = pk)
	appt = Appointment.objects.all().filter(patient_id=pk)
	docId=[]
	for a in appt:
		docId.append(a.doctor_id)
	doc = Doctor.objects.all().filter(id__in = docId)
	# decrypt doc
	for do in doc:
		do = decryptDoctor(do)
	# decrypt patient
	patient = decryptPatient(patient)
	# decrypt appoinntment
	for ap in appt:
		ap = decryptAppointment(ap)
	d = {'doc': doc, 'appot': appt, 'patient': patient}
	return render(request, 'patient.html', d)

@login_required(login_url='login')
@user_passes_test(is_admin)
def deletePatient(request, pk):
	if not request.user.is_authenticated:
		return redirect('login')
	pat = Patient.objects.get(id=pk)
	pat.delete()
	return redirect('patientsList')

# Admin - doctor views

@login_required(login_url='login')
@user_passes_test(is_admin)
def addDoctor(request):
	error = ""
	if not request.user.is_authenticated:
		return redirect('login')
	if request.method == "POST":
		fName = request.POST.get('fName')
		lName = request.POST.get('lName')
		spec = request.POST.get('spec')
		phone = request.POST.get('phone')
		doctorId = request.POST.get('doctor')
		# doctor01 =  User.objects.get(id=doctorId)
		# encrypt doc data here
		key_value = Fernet.generate_key()
		fName = wordEnc(fName, key_value).decode()
		lName = wordEnc(lName, key_value).decode()
		spec = wordEnc(spec, key_value).decode()
		phone = wordEnc(phone, key_value).decode()
		key_value = key_value.decode()
		try:
			doc = Doctor(firstName = fName, lastName = lName, speciality = spec, phone = phone, key_value = key_value)
			doc.save()
			error = "no"
		except:
			error = "yes"
	d = {'error':error}
	return render(request, 'addDoctor.html', d)

@login_required(login_url='login')
@user_passes_test(is_admin)
def addDoctor_pk(request, pk):
	error = ""
	if not request.user.is_authenticated:
		return redirect('login')
	if request.method == "POST":
		fName = request.POST.get('fName')
		lName = request.POST.get('lName')
		spec = request.POST.get('spec')
		phone = request.POST.get('phone')
		doctor01 =  User.objects.get(id=pk)
		# encrypt doc data here
		key_value = Fernet.generate_key()
		fName = wordEnc(fName, key_value).decode()
		lName = wordEnc(lName, key_value).decode()
		spec = wordEnc(spec, key_value).decode()
		phone = wordEnc(phone, key_value).decode()
		key_value = key_value.decode()
		try:
			doc = Doctor(user = doctor01, firstName = fName, lastName = lName, speciality = spec, phone = phone, key_value = key_value)
			doc.save()
			error = "no"
		except:
			error = "yes"
	d = {'error':error, 'id': pk}
	return render(request, 'addDoctor_pk.html', d)


@login_required(login_url='login')
@user_passes_test(is_admin)
def viewDoctor(request):
	if not request.user.is_authenticated:
		return redirect('login')
	doc = Doctor.objects.all()
	# decrypt doc data here
	for do in doc:
		do = decryptDoctor(do)
	d = {'doc': doc}
	return render(request, 'viewDoctor.html', d)

@login_required(login_url='login')
@user_passes_test(is_admin)
def doctor(request, pk):
	if not request.user.is_authenticated:
		messages.success(request, ('You need to login first!'))
		return redirect('login')
	doc = Doctor.objects.get(id = pk)
	appt = Appointment.objects.all().filter(doctor_id=pk)
	patientid=[]
	for a in appt:
		patientid.append(a.patient_id)
	patient = Patient.objects.all().filter(id__in = patientid)
	# decrypt doc
	doc = decryptDoctor(doc)
	# decrypt patient
	for pa in patient:
		pa = decryptPatient(pa)
	# decrypt appoinntment
	for ap in appt:
		ap = decryptAppointment(ap)
	d = {'doc': doc, 'appot': appt, 'patient': patient}
	return render(request, 'doctor.html', d)

@login_required(login_url='login')
@user_passes_test(is_admin)
def deleteDoctor(request, pk):
	if not request.user.is_authenticated:
		return redirect('login')
	doc = Doctor.objects.get(id=pk)
	doc.delete()
	return redirect('viewDoctor')

# Admin - appointment view

@login_required(login_url='login')
@user_passes_test(is_admin)
def addAppointment(request):
	error = ""
	if not request.user.is_authenticated:
		return redirect('login')
	doc = Doctor.objects.all()
	patients = Patient.objects.all()
	if request.method == "POST":
		doctorId = request.POST.get('doctor')
		patientId = request.POST.get('patient')
		date = request.POST.get('date')
		time = request.POST.get('time')
		doctor01 = Doctor.objects.filter(id=doctorId).first()
		patient01 = Patient.objects.filter(id=patientId).first()
		# encrypt appointment
		key_value = Fernet.generate_key()
		date = wordEnc(date, key_value).decode()
		time = wordEnc(time, key_value).decode()
		try:
			Appointment.objects.create(doctor = doctor01, patient = patient01, date = date, time = time, key_value=key_value.decode())
			error = "no"
		except:
			error = "yes"
	# encrypt doc
	for do in doc:
		do = decryptDoctor(do)
	# decrypt patient
	for pa in patients:
		pa = decryptPatient(pa)
	# encrypt appoinntment
	d = {'error':error, 'doc':doc, 'patients':patients}
	return render(request, 'addAppointment.html', d)

@login_required(login_url='login')
@user_passes_test(is_admin)
def viewAppointment(request):
	if not request.user.is_authenticated:
		return redirect('login')
	appoint = Appointment.objects.all()
	# decrypt appointment data here
	for app in appoint:
		app = decryptAppointment(app)
	d = {'appoint': appoint}
	return render(request, 'viewAppointment.html', d)

@login_required(login_url='login')
@user_passes_test(is_admin)
def deleteAppointment(request, pk):
	if not request.user.is_authenticated:
		return redirect('login')
	doc = Appointment.objects.get(id=pk)
	doc.delete()
	return redirect('viewAppointment')

@login_required(login_url='login')
@user_passes_test(is_admin)
def	appointment(request):
	return render(request, 'appointment.html', {})

# Views for doctor

@login_required(login_url='login')
@user_passes_test(is_doctor)
def doctorHome(request):
	doctor = Doctor.objects.get(user_id = request.user.id)
	docId = doctor.id
	patientcount = Appointment.objects.all().filter(doctor_id = docId).distinct().count()
	appointmentcount = Appointment.objects.all().filter(doctor_id=docId).distinct().count()
	appointments = Appointment.objects.all().filter(doctor_id=docId)
	patientid=[]
	for a in appointments:
		patientid.append(a.patient_id)
	patients = Patient.objects.all().filter(id__in=patientid)
	# decrypt doctor
	doctor = decryptDoctor(doctor)
	# decrypt patient
	for pa in patients:
		pa = decryptPatient(pa)
	# decrypt appointment
	for ap in appointments:
		ap = decryptAppointment(ap)
	d = {
    'patientcount':patientcount,
    'appointmentcount':appointmentcount,
    'appointments':appointments,
	'patients': patients,
    'doctor': doctor
    }
	return render(request, 'doctorHome.html', d)

@login_required(login_url='login')
@user_passes_test(is_doctor)
def doctor_view_patient(request, pk):
	if not request.user.is_authenticated:
		messages.success(request, ('You need to login first!'))
		return redirect('login')
	patient = Patient.objects.get(id = pk)
	docId = Doctor.objects.get(user_id = request.user.id).id
	appt = Appointment.objects.all().filter(patient_id=pk, doctor_id = docId)
	docId=[]
	for a in appt:
		docId.append(a.doctor_id)
	doc = Doctor.objects.all().filter(id__in = docId)
	# decrypt patient
	patient = decryptPatient(patient)
	# decrypt doctor
	for do in doc:
		do = decryptDoctor(do)
	# encrypt appointment
	for ap in appt:
		ap = decryptAppointment(ap)
	d = {'doc': doc, 'appot': appt, 'patient': patient}
	return render(request, 'doctor_view_patient.html', d)

@login_required(login_url='login')
@user_passes_test(is_doctor)
def doctor_editAppointment(request, pk):
	
	return render(request, 'doctor_editAppointment.html', {})

@login_required(login_url='login')
@user_passes_test(is_doctor)
def doctor_add_appointment(request):
	error = ""
	if not request.user.is_authenticated:
		return redirect('login')
	doc = Doctor.objects.get(user_id = request.user.id)
	patients = Patient.objects.all()
	if request.method == "POST":
		patientId = request.POST.get('patient')
		date = request.POST.get('date')
		time = request.POST.get('time')
		# doctor01 = Doctor.objects.filter(id=doc).first()
		patient01 = Patient.objects.filter(id=patientId).first()
		# encrypt appointment
		key_value = Fernet.generate_key()
		date = wordEnc(date, key_value).decode()
		time = wordEnc(time, key_value).decode()
		try:
			Appointment.objects.create(doctor = doc, patient = patient01, date = date, time = time, key_value = key_value.decode())
			error = "no"
		except:
			error = "yes"
	# decrypt doctor
	doc = decryptDoctor(doc)
	# decrypt patient
	for pa in patients:
		pa = decryptPatient(pa)
	d = {'error':error, 'patients':patients}
	return render(request, 'doctor_add_appointment.html', d)

@login_required(login_url='login')
@user_passes_test(is_doctor)
def doctor_deleteAppointment(request, pk):
	if not request.user.is_authenticated:
		return redirect('login')
	doc = Appointment.objects.get(id=pk)
	doc.delete()
	return redirect('doctorHome')

# Views for Patients

@login_required(login_url='login')
@user_passes_test(is_patient)
def patientHome(request):
	patient = Patient.objects.get(user_id = request.user.id)
	patId = patient.id
	doctorcount = Appointment.objects.all().filter(patient_id = patId).distinct().count()
	appointmentcount = Appointment.objects.all().filter(patient_id=patId).distinct().count()
	appointments = Appointment.objects.all().filter(patient_id=patId)
	docId=[]
	for a in appointments:
		docId.append(a.doctor_id)
	doctors =  Doctor.objects.all().filter(id__in = docId)
	# decrypt doc
	for doc in doctors:
		doc = decryptDoctor(doc)
	# decrypt patient
	patient = decryptPatient(patient)
	# decrypt appointment
	for app in appointments:
		app = decryptAppointment(app)
	d = {
    'doctorCount':doctorcount,
    'appointmentcount':appointmentcount,
    'appointments':appointments,
	'patient': patient,
    'doctor': doctors
    }
	return render(request, 'patientHome.html', d)

@login_required(login_url='login')
@user_passes_test(is_patient)
def patient_view_doctor(request, pk):
	if not request.user.is_authenticated:
		messages.success(request, ('You need to login first!'))
		return redirect('login')
	doctor = Doctor.objects.get(id = pk)
	patId = Patient.objects.get(user_id = request.user.id).id
	appt = Appointment.objects.all().filter(doctor_id=pk, patient_id = patId)
	patientId=[]
	for a in appt:
		patientId.append(a.patient_id)
	patients = Patient.objects.all().filter(id__in = patientId)
	# encrypt doc
	doctor = decryptDoctor(doctor)
	# encrypt patient
	for pa in patients:
		pa = decryptPatient(pa)
	# encrypt appoinntment
	for ap in appt:
		ap = decryptAppointment(ap)
	d = {'doc': doctor, 'appot': appt, 'patient': patients}
	return render(request, 'patient_view_doctor.html', d)

@login_required(login_url='login')
@user_passes_test(is_patient)
def patientViewAllDoctors(request):
	if not request.user.is_authenticated:
		return redirect('login')
	doc = Doctor.objects.all()
	# decrypt doc data here
	for do in doc:
		do = decryptDoctor(do)
	d = {'doc': doc}
	return render(request, 'patientViewAllDoctors.html', d)

@login_required(login_url='login')
@user_passes_test(is_patient)
def patientAddAppointments(request):
	error = ""
	if not request.user.is_authenticated:
		return redirect('login')
	pat = Patient.objects.get(user_id = request.user.id).id
	doctors = Doctor.objects.all()
	print(doctors)
	if request.method == "POST":
		doctorId = request.POST.get('doctor')
		date = request.POST.get('date')
		time = request.POST.get('time')
		patient01 = Patient.objects.filter(id=pat).first()
		doctor01 = Doctor.objects.filter(id = doctorId).first()
		key_value = Fernet.generate_key()
		date = wordEnc(date, key_value).decode()
		time = wordEnc(time, key_value).decode()
		try:
			Appointment.objects.create(doctor=doctor01, patient=patient01, date=date, time=time, key_value=key_value.decode())
			error = "no"
		except:
			error = "yes"
	# encrypt doc
	for doc in doctors:
		doc = decryptDoctor(doc)
	d = {'error': error, 'doc':doctors}
	return render(request, 'patientAddAppointments.html', d)

@login_required(login_url='login')
@user_passes_test(is_patient)
def guestAddPatient(request, pk):
	error = ""
	if not request.user.is_authenticated:
		return redirect('login')
	if request.method == "POST":
		fName = request.POST.get('fName')
		lName = request.POST.get('lName')
		address = request.POST.get('address')
		contact = request.POST.get('contact')
		dob = request.POST.get('dob')
		gender = request.POST.get('gender')
		weight = request.POST.get('weight')
		height = request.POST.get('height')
		healthHistory = request.POST.get('helhis')
		medication = request.POST.get('medication')
		patient01 = User.objects.get(id=pk)
		# encrypt pat data here 
		key_value = Fernet.generate_key()
		fName = wordEnc(fName, key_value).decode()
		lName = wordEnc(lName, key_value).decode()
		address = wordEnc(address, key_value).decode()
		contact = wordEnc(contact, key_value).decode()
		dob = wordEnc(dob, key_value).decode()
		healthHistory = wordEnc(healthHistory, key_value).decode()
		medication = wordEnc(medication, key_value).decode()
		weight = orderedNumber(weight)
		height = orderedNumber(height)
		gender = getGenderBin(gender)
		try:
			Patient.objects.create(user = patient01, firstName = fName, lastName = lName, address = address, contact = contact, dob = dob, gender = gender, weight = weight, height = height, healthHistory = healthHistory, medication = medication, key_value = key_value.decode())
			error = "no"
		except:
			error = "yes"
	d = {'error':error, 'id': pk}
	return render(request, 'guestAddPatient.html', d)

