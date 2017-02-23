from django.test import TestCase, RequestFactory
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
import logging
from .test_utility import test_util
import requests
from .views import market_home
import json

logger = logging.getLogger(__name__)
USER_NUM = 5

class AuthenticationTest(TestCase):

	random_users = []

	def generate_random_users(self):

		logging.basicConfig()
		logger.setLevel(logging.INFO)
		util = test_util()

		for i in xrange(1, USER_NUM):
			random_user = {}
			random_user['username'] = util.random_username()
			random_user['email'] = util.random_email()
			random_user['password'] = util.random_password(util.random_num_range(8, 12))
			self.random_users.append(random_user)
			logger.info("Generated USER with %s, %s, %s", random_user['username'], random_user['email'], random_user['password'])

		logger.info("Random credentials generation completed")

	def setUp(self):
		"""Creates array of users temporarily for the purpose of testing
		
		Returns:
		    None
		"""
		self.generate_random_users()

		for user in self.random_users:
			User.objects.create_user(username=user['username'], password=user['password'], email=user['email'])
			logger.info("Inserted USER with %s, %s, %s", user['username'], user['email'], user['password'])

		logger.info("Insertion of %d users completed", len(self.random_users))

	def test_check_for_successful_authentication(self):
		"""Test suite which checks for successful authentication of users 
		
		Returns:
		    None
		"""

		for user in self.random_users:
			logger.info("Trying to authenticate %s with password %s", user['username'], user['password'])
			user = authenticate(username=user['username'], password=user['password'])
			self.assertIsNotNone(user)

		logger.info("User authentication performed successfully")

	def test_check_for_unsuccessful_authentication(self):
		"""Sends wrong few username/password for check of failed login
		
		Returns:
		    None
		"""
		user = authenticate(username='user2', password='wrongpassword')
		self.assertIsNone(user)
		user = authenticate(username='wrongusername', password='user2@*passwd')
		self.assertIsNone(user)
		
		logger.info("Wrong authentication test performed successfully")

	def tearDown(self):
		"""Removes array of users created temporarily during the setUp phase
		
		Returns:
		    None
		"""
		for user in self.random_users:
			user_handler = User.objects.get(username=user['username'])
			user_handler.delete()
			logger.info("Removed %s user with email %s and password %s successfully", user['username'], user['email'], user['password'])

class LocationTest(TestCase):

	def setUp(self):
		"""Summary
		
		Returns:
		    TYPE: Description
		"""
		print("!@#@#")
		logging.basicConfig()
		logger.setLevel(logging.INFO)
		self.factory = RequestFactory()
		logger.info("Starting location test")

	def test_response(self):
		"""Summary
		
		Returns:
		    TYPE: Description
		"""
		logger.info("Testing for response message for malformed request")
		request = self.factory.post('/interface/market')
		response = market_home(request)
		self.assertTrue(response.text == 'Only POST request is accepted')
		logger.info("Successfully received \"" + response.text + "\" message.")

	def test_location(self):
		"""Summary
		
		Returns:
		    TYPE: Description
		"""
		logger.info("Testing for correctness in nearest market function by sending location coordinates")
		request = self.factory.post('/interface/market', data={'latitude': 3, 'longitude': 84})
		response = market_home(request)
		json_obj = json.loads(response.text)
		self.assertTrue(json_obj['name'] == 'Chennai-central')
		logger.info("Successfully received Chennai-central market for coordinates [3, 84]")

		logger.info("Testing for correctness in nearest market function by sending location coordinates")
		request = self.factory.post('/interface/market', data={'latitude': 13.5, 'longitude': 80.1})
		response = market_home(request)
		json_obj = json.loads(response.text)
		self.assertTrue(json_obj['name'] == 'Tada')
		logger.info("Successfully received Tada market for coordinates [13.5, 80.1]")