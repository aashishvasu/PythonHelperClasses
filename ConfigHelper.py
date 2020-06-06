#Aashish Vasudevan
#A class to create and maintain a counter for google sheets related spreadsheets

from configparser import ConfigParser

import os

class BotConfig:
	config = ConfigParser()

	# Returns a clean and usable config
	def ConfigChecker(self, config, id):
		# Check if config file has required keys
		if not config.has_section('Spreadsheet'):
			config.add_section('Spreadsheet')
			
		if not config.has_option('Spreadsheet', 'ID'):
			config.set('Spreadsheet', 'ID', id)

		if not config.has_option('Spreadsheet', 'current-row'):
			config.set('Spreadsheet', 'current-row', '0')

		return config

	def CreateConfigFile(self, fileName, SpreadsheetList):
		# Ask user to choose from list of spreadsheets
		counter = 0
		for item in SpreadsheetList:
			print(u'{0}: {1}'.format(counter, item['name']))
			counter += 1
		idStr = input("Choose spreadsheet to use: ")
		try:
			idNum = int(idStr)
			print(u'Using file ({0})'.format(SpreadsheetList[idNum]['name']))
		except ValueError:
			# Exit if non numerical value is chosen
			raise SystemExit("Not a numerical value!")

		self.config = self.ConfigChecker(self.config, SpreadsheetList[idNum]['id'])
		self.SaveConfigFile(fileName)		

	def SaveConfigFile(self, fileName):
		with open(fileName, 'w') as f:
			self.config.write(f)
	
	def GetID(self):
		return self.config['Spreadsheet']['ID']

	def GetCurrentRow(self):
		return self.config['Spreadsheet']['current-row']

	def SetCurrentRow(self, index):
		self.config.set('Spreadsheet', 'current-row', str(index))