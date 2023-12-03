import random
from datetime import date



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