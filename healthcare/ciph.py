import random
from datetime import date

import numpy as np

import hashlib
from cryptography.fernet import Fernet
import base64

from django.db import connections
import mysql.connector

def checkDups(fName, lName):

	cursor = connections['default'].cursor()
	queryDup = 'SELECT * FROM patients;'	
	result = cursor.execute(queryDup)
	result = cursor.fetchall()

	for patient in result:
		patient = decryptResultData(patient)
		if patient[0] == fName and patient[1] == lName:
			return True
		else:
			return False

def decryptPatientData(patientThis, keyVal):
	try:
		patientThis.firstName = wordDec(patientThis.firstName, keyVal[0]) #firstname
		patientThis.lastName = wordDec(patientThis.lastName, keyVal[0]) #lastname
		patientThis.healthHistory = wordDec(patientThis.healthHistory, keyVal[0]) #healthHistory
		patientThis.gender = getGender(patientThis.gender) #gender 
		patientThis.weight = realWeight(patientThis.weight) #weight
		patientThis.height = realHeight(patientThis.height) #height
		patientThis.dob = wordDecrypt(patientThis.dob, keyVal[0]) #height
		return patientThis
	except:
		return patientThis

def decryptResultData(patientThis):
	firstName1 = wordDec(patientThis[1], patientThis[7]) #firstname
	lastName1 = wordDec(patientThis[2], patientThis[7]) #lastname
	healthHistory1 = wordDec(patientThis[6], patientThis[7]) #healthHistory
	gender1 = getGender(patientThis[3]) #gender 
	weight1 = realWeight(patientThis[4]) #weight
	height1 = realHeight(patientThis[5]) #height
	dob1 = wordDec(patientThis[8], patientThis[7]) #height
	patientThis = (firstName1, lastName1, gender1, weight1, height1, healthHistory1, dob1, patientThis[7])
	return patientThis

def decryptPatient(patientThis, keyVal):
	patientThis.firstName = wordDecrypt(patientThis.firstName, keyVal) #firstname
	patientThis.lastName = wordDecrypt(patientThis.lastName, keyVal) #lastname
	patientThis.healthHistory = wordDecrypt(patientThis.healthHistory, keyVal) #healthHistory
	patientThis.dob = wordDecrypt(patientThis.dob, keyVal) #healthHistory
	patientThis.gender = getGender(patientThis.gender) #gender 
	patientThis.weight = realWeight(patientThis.weight) #weight
	patientThis.height = realHeight(patientThis.height) #height
	return patientThis

def encrypt_pwd(pwd):
	sha_signature = \
		hashlib.sha256(pwd.encode()).hexdigest()
	return sha_signature

def rand_key():
	key = ""
	for i in range(2):
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
	if gender[2] == '1':
		line = 'Male'
	else:
		line = 'Female'
	return line

def orderedWeight(weight):
	weight = int(weight)
	oWeight = 2023 + (weight * 99 / 8)
	oWeight = str(round(oWeight, 2))
	return oWeight

def realWeight(oWeight):
	oWeight = int(float(oWeight))
	rWeight = (oWeight - 2023) * 8 / 99 
	rWeight = str(round(rWeight, 2))
	return rWeight


def orderedHeight(height):
	height = int(height)
	height = 1995 + (height * 65 / 52)
	height = str(round(height, 2))
	return height

def realHeight(height):
	height = int(float(height))
	height = (height - 1995) * 52 / 65 
	height = str(round(height, 2))
	return height


def wordEnc(pwd, key):
	pwd = bytes(pwd, 'utf-8')
	cipher_suite = Fernet(key)
	encodedPwd = cipher_suite.encrypt(pwd)
	return encodedPwd


def wordDec(pwd, key):
	key = bytes(key, 'utf-8')
	cipher_suite = Fernet(key)
	try:
		pwd = pwd.encode()
		decPwd = cipher_suite.decrypt(pwd)
	except:
		pwd = bytes(pwd, 'utf-8')
		decPwd = cipher_suite.decrypt(pwd)
	decPwd = str(decPwd, encoding='utf-8')
	return decPwd

def wordDecrypt(pwd, key):
	key = bytes(key, 'utf-8')
	pwd = bytes(pwd, 'utf-8')
	cipher_suite = Fernet(key)
	decPwd = cipher_suite.decrypt(pwd)
	decPwd = str(decPwd, encoding='utf-8')
	return decPwd










