import random
from datetime import date

import hashlib

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
	line = gender[2]
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