from django.test import TestCase, Client
from django.urls import reverse
from django.core import mail
from django.utils import timezone
from datetime import timedelta
from .models import CustomUser


class OTPSignupTests(TestCase):
	def setUp(self):
		self.client = Client()
		self.signup_url = reverse('signup')
		self.verify_url = reverse('verify_otp')

	def test_signup_creates_user_and_sends_otp(self):
		email = 'testuser@example.com'
		response = self.client.post(self.signup_url, {'email': email})
		self.assertEqual(response.status_code, 200)
		data = response.json()
		self.assertIn('status', data)
		self.assertEqual(data['status'], 'success')
		user = CustomUser.objects.get(email=email)
		self.assertIsNotNone(user.otp)
		self.assertIsNotNone(user.otp_created_at)
		# Ensure an email was sent
		self.assertEqual(len(mail.outbox), 1)

	def test_verify_otp_success_clears_otp_and_logs_in(self):
		email = 'verifyuser@example.com'
		user = CustomUser.objects.create_user(email=email, password='123456', user_type='5')
		otp = '123456'
		user.otp = otp
		user.otp_created_at = timezone.now()
		user.set_password(otp)
		user.save()
		response = self.client.post(self.verify_url, {'email': email, 'otp': otp})
		self.assertEqual(response.status_code, 200)
		data = response.json()
		self.assertEqual(data['status'], 'success')
		user.refresh_from_db()
		self.assertEqual(user.otp, '')
		self.assertIsNone(user.otp_created_at)

	def test_verify_otp_expired(self):
		email = 'expired@example.com'
		user = CustomUser.objects.create_user(email=email, password='123456', user_type='5')
		otp = '654321'
		user.otp = otp
		user.set_password(otp)
		user.otp_created_at = timezone.now() - timedelta(minutes=30)
		user.save()
		response = self.client.post(self.verify_url, {'email': email, 'otp': otp})
		self.assertEqual(response.status_code, 400)
		data = response.json()
		self.assertEqual(data['status'], 'error')
		self.assertIn('OTP has expired', data['message'])
