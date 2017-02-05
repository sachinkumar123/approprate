import random
from faker import Factory

class test_util:

	faker = None
	def __init__(self):
		self.faker = Factory.create()

	def random_username(self):
		return self.faker.user_name()
	   #return ''.join(random.choice(string.lowercase) for i in range(length))

	def random_password(self, length):
		return self.faker.password(length)
		#chars = string.ascii_letters + string.digits + '!@#$%^&*()'
		#return ''.join(random.choice(chars) for i in range(length))

	def random_email(self):
		return self.faker.email()

	def random_num_range(self, min, max):
		return random.randint(min, max)