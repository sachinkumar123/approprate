from django.test import TestCase
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
import logging

logger = logging.getLogger(__name__)

# Create your tests here.

class AuthenticationTest(TestCase):
	def setUp(self):
		"""Creates array of users temporarily for the purpose of testing
		
		Returns:
		    None
		"""
		User.objects.create_user('user1', 'user1@iiits.in', 'passwd@*user1')
		User.objects.create_user('user2', 'user2@iiits.in', 'user2@*passwd')
		logger.info("Created sample username successfully")

	def test_check_for_successful_authentication(self):
		"""Test suite which checks for successful authentication of users 
		
		Returns:
		    None
		"""
		user = authenticate(username='user1', password='passwd@*user1')
		self.assertIsNotNone(user)
		user = authenticate(username='user2', password='user2@*passwd')
		self.assertIsNotNone(user)
		
		logger.info("User authentication performed successfully")

	def test_check_for_unsuccessful_authentication(self):
		"""Sends wrong username/password for check of failed login
		
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
		user = User.objects.get(username='user1')
		user.delete()

		user = User.objects.get(username='user2')
		user.delete()

		logger.info("Removed temporary users")