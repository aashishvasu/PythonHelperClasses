#Aashish Vasudevan
#A class to help with google API authentication (scope based)

from __future__ import print_function
import pickle
import os.path
import json
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

class GoogleAuth:
	SCOPE = None

	tokenFolderName = 'Oauth2'
	loginTokenName = 'token.pickle'
	credentialFileName = ''

	def __init__(self, apiScope, credentialFileName = ''):
		self.credentialFileName = credentialFileName		
		self.SCOPE = apiScope

	def TryAuth(self):
		creds = None

		# Create credential directory if it doesnt exist
		if os.path.exists(self.tokenFolderName) == False:
			os.mkdir(self.tokenFolderName)
		
		# The file token.pickle stores the user's access and refresh tokens, and is
		# created automatically when the authorization flow completes for the first
		# time.
		if os.path.exists(self.tokenFolderName + "/" + self.loginTokenName):
			with open(self.tokenFolderName + "/" + self.loginTokenName, 'rb') as token:
				creds = pickle.load(token)
				
		# If there are no (valid) credentials available, let the user log in.
		if not creds or not creds.valid:
			if creds and creds.expired and creds.refresh_token:
				creds.refresh(Request())
			else:
				flow = None
				flow = InstalledAppFlow.from_client_secrets_file(self.credentialFileName, self.SCOPE)

				creds = flow.run_local_server(authorization_prompt_message="Please allow access to app in your browser", success_message="Login Successful!")
			# Save the credentials for the next run
			with open(self.tokenFolderName + "/" + self.loginTokenName, 'wb') as token:
				pickle.dump(creds, token)

		return creds

	def BuildUserService(self, api, apiVersion, oauthCredentials):
		return build(api, apiVersion, credentials=oauthCredentials, cache_discovery=False)

	@staticmethod
	def AuthenticateGoogle(credentialsFileName, scope):
		print("Authenticating Google")
		# Authenticate google API
		googleService = GoogleAuth( credentialFileName=credentialsFileName,
									apiScope=scope
									)

		credentials = googleService.TryAuth()

		# Build GDrive and GSheets services
		drive = googleService.BuildUserService('drive', 'v3', credentials)
		sheet = googleService.BuildUserService('sheets', 'v4', credentials)

		return drive, sheet