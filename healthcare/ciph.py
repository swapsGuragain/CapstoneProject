import random
from datetime import date

import numpy as np

import hashlib
from cryptography.fernet import Fernet
import base64

from django.db import connections
import mysql.connector

def decryptAppointment(appointment):
	appointment.doctor = decryptDoctor(appointment.doctor)
	appointment.patient = decryptPatient(appointment.patient)
	appointment.date = wordDec(appointment.date, appointment.key_value)
	appointment.time = wordDec(appointment.time, appointment.key_value)
	return appointment

def decryptDoctor(doctor):
	doctor.firstName = wordDec(doctor.firstName, doctor.key_value)
	doctor.lastName = wordDec(doctor.lastName, doctor.key_value)
	doctor.speciality = wordDec(doctor.speciality, doctor.key_value)
	doctor.phone = wordDec(doctor.phone, doctor.key_value)
	return doctor

def decryptPatient(patient):
	patient.firstName = wordDec(patient.firstName, patient.key_value)
	patient.lastName = wordDec(patient.lastName, patient.key_value)
	patient.address = wordDec(patient.address, patient.key_value)
	patient.contact = wordDec(patient.contact, patient.key_value)
	patient.dob = wordDec(patient.dob, patient.key_value)
	patient.healthHistory = wordDec(patient.healthHistory, patient.key_value)
	patient.medication = wordDec(patient.medication, patient.key_value)
	patient.gender = getGender(patient.gender)
	patient.weight = realNumber(patient.weight)
	patient.height = realNumber(patient.height)
	return patient

def rand_key():
	key = ""
	for i in range(5):
		temp = str(random.randint(0, 1))
		key += temp
	return(key)

def getAge(dob):
	today = date.today()
	year, month, day = map(int, dob.split('-'))
	dob = date(year, month, day)
	age = today.year - dob.year - ((today.month, today.day)<(dob.month, dob.day))
	return age
	
def getGenderBin(gender):
	if gender == 'male' or gender == 'Male' or gender == 'MALE' or gender == 'm' or gender == 'M':
		gender = '1'
	else:
		gender = '0'
	gender = rand_key() + gender + rand_key()
	return gender

def getGender(gender):
	if gender[5] == '1':
		line = 'Male'
	else:
		line = 'Female'
	return line

def orderedNumber(num):
	num = int(num)
	onum = 2023000002024 + (num * 99 / 8)
	onum = str(round(onum, 2))
	return onum

def realNumber(oWeight):
	oWeight = int(float(oWeight))
	rWeight = (oWeight - 2023000002024) * 8 / 99 
	rWeight = str(round(rWeight, 2))
	return rWeight

def wordEnc(pwd, key):
	pwd = bytes(pwd, 'utf-8')
	cipher_suite = Fernet(key)
	encodedPwd = cipher_suite.encrypt(pwd)
	return encodedPwd

def wordDec1(pwd, key):
	key = key.encode("utf-8")
	key = base64.b64encode(key)
	cipher_suite = Fernet(key)
	try:
		pwd = pwd.encode()
		decPwd = cipher_suite.decrypt(pwd)
	except:
		pwd = bytes(pwd, 'utf-8')
		decPwd = cipher_suite.decrypt(pwd)
	decPwd = str(decPwd, encoding='utf-8')
	return decPwd

def wordDec(pwd, key):
	try:
		key = key.encode()
	except:
		key = bytes(key, 'utf-8')
	cipher_suite = Fernet(key)
	try:
		pwd = pwd.encode()
	except:
		pwd = bytes(key, 'utf-8')
	decPwd = cipher_suite.decrypt(pwd)
	decPwd = str(decPwd, encoding='utf-8')
	return decPwd











