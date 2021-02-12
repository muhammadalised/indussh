import random

def generate_upc():
	upc = ''
	for i in range(9):
	 upc += str(random.randint(0,9))

	return upc