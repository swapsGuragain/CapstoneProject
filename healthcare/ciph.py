import random
from datetime import date

import numpy as np

import hashlib
from cryptography.fernet import Fernet
import base64

from django.db import connections
import mysql.connector

def checkDups(fName, lName, hHistory):

	cursor = connections['default'].cursor()
	queryDup = 'SELECT * FROM patients;'	
	result = cursor.execute(queryDup)
	result = cursor.fetchall()

	for patient in result:
		patientThis = list(patient)
		keyVal = patientThis[7]


		# patientThis[1] = wordDec(patientThis[1], keyVal) #firstname
		# patientThis[2] = wordDec(patientThis[2], keyVal) #lastname
		# patientThis[3] = getGender(patientThis[3])
		# patientThis[4] = realWeight(patientThis[4])
		# patientThis[5] = realHeight(patientThis[5])
		# patientThis[6] = wordDec(patientThis[6], keyVal) #healthHistory
		# patientThis[7] = wordDec(patientThis[7], keyVal) #dob


		try:
			patientThis[1] = wordDec(bytes(patientThis[1], 'utf-8'), keyVal) #firstname
			patientThis[2] = wordDec(bytes(patientThis[2], 'utf-8'), keyVal) #lastname
			patientThis[3] = getGender(patientThis[3])
			patientThis[4] = realWeight(patientThis[4])
			patientThis[5] = realHeight(patientThis[5])
			patientThis[6] = wordDec(bytes(patientThis[6], 'utf-8'), keyVal) #healthHistory
			if patient[1] == fName and patient[2] == lName and patient[6] == hHistory:
				return True
			else:
				return False
		except:
			for i in patientThis:
				if i == None:
					i = 0
			patientThis[1] = wordDec(patientThis[1], keyVal)
			patientThis[2] = wordDec(patientThis[2], keyVal)
			patientThis[3] = getGender(patientThis[3])
			patientThis[4] = realWeight(patientThis[4])
			patientThis[5] = realHeight(patientThis[5])
			patientThis[6] = wordDec(patientThis[6], keyVal)
			if patient[1] == fName and patient[2] == lName and patient[6] == hHistory:
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
		return patientThis
	except:
		return patientThis

def decryptResultData(patientThis):
	try:
		print(patientThis[1])
		patientThis[1] = wordDec(patientThis[1], patientThis[7]) #firstname
		# patientThis[2] = wordDec(patientThis.lastName, patientThis[7]) #lastname
		# patientThis[6] = wordDec(patientThis.healthHistory, patientThis[7]) #healthHistory
		# patientThis[3] = getGender(patientThis[3]) #gender 
		# patientThis[4] = realWeight(patientThis[4]) #weight
		# patientThis[5] = realHeight(patientThis[5]) #height
		print('got here')
		return patientThis
	except:
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
	if gender[2] == 1:
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
		print(pwd, "hhhhhhhhhhhhhhhhhhhhhhhhhhhh")
		pwd = pwd.encode()
		decPwd = cipher_suite.decrypt(pwd)
	except:
		pwd = bytes(pwd, 'utf-8')

		print(pwd, "[[[[[[[[[[[[[[[[[[[[[]]]]]]]]]]]]]]]]]]]]]")
		decPwd = cipher_suite.decrypt(pwd)
	decPwd = str(decPwd, encoding='utf-8')
	return decPwd