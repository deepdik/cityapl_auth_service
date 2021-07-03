import re
import datetime
from django.conf import settings

from google.oauth2 import id_token
from google.auth.transport import requests

from cityapl.apps.user_auth.models import UserOTP


class SendSMS:
	"""
	"""
	@staticmethod
	def fast2_sms_send(number, message):
		"""
		"""
		url = "https://www.fast2sms.com/dev/bulkV2"
		payload = "sender_id={}&message={}&route=v3&numbers={}".format(
			'CITYAPL',
			message,
			number
			)
		headers = {
			'authorization': settings.FAST2SMS_API,
			'Content-Type': "application/x-www-form-urlencoded",
			'Cache-Control': "no-cache",
			}
		response = requests.request("POST", url, data=payload, headers=headers)
		return response.status_code


class SocialOauth2:
	"""
	"""
	@staticmethod
	def google_token_verify(access_token):
		"""
		"""
		try:
			# Specify the CLIENT_ID of the app that accesses the backend:
			idinfo = id_token.verify_oauth2_token(
				access_token,
				requests.Request(),
				settings.SOCIAL_AUTH_GOOGLE_OAUTH_KEY
			)

			# Or, if multiple clients access the backend server:
			# idinfo = id_token.verify_oauth2_token(token, requests.Request())
			# if idinfo['aud'] not in [CLIENT_ID_1, CLIENT_ID_2, CLIENT_ID_3]:
			#     raise ValueError('Could not verify audience.')

			# If auth request is from a G Suite domain:
			# if idinfo['hd'] != GSUITE_DOMAIN_NAME:
			#     raise ValueError('Wrong hosted domain.')

			# ID token is valid. Get the user's Google Account ID from the decoded token.
			print(idinfo)
			return [True, idinfo]
		except Exception as e:
			# Invalid token
			print(e)
			return [False]
		

class CustomValidators:
	"""
	"""
	@staticmethod
	def validate_mobile(mobile_number):
		"""
		contains 7 or 8 or 9.
		contains 9 digits
		"""		
		Pattern = re.compile("[7-9][0-9]{9}")
		return Pattern.match(mobile_number)
			 

class OTPAuth:
	"""
	"""
	@staticmethod
	def generate_otp(user):
		"""
		"""
		OTP = random.randint(1000,9999)
		# save OTP with this user
		UserOTP.objects.update_or_create(
			user=user,
			defaults={
				'otp':OTP,
				'exp_time':datetime.datetime.now()+datetime.timedelta(minutes = 10)
				}
			)

		return OTP

	def validate_otp(user, otp):
		"""
		"""
		otp_qs = UserOTP.objects.filter(user=user)
		if otp_qs.exists():
			if otp_qs.first().exp_time > datetime.datetime.now():
				if otp_qs.first().otp == otp:
					return [True]
				return [False, 'Invalid OTP']
			return [False, 'OTP expired']
		return [False, 'No OTP found']
