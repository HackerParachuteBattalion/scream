import sys, urllib2, httplib, urllib, xmlHandler, dbscream, json, re, pprint
from sqlite3 import OperationalError
import scream

class Session:
		def __init__(self, main, DEBUG=False):
			self.locname = "WESTPOINT0"
			self.main = main
			self.DEBUG = DEBUG
			if self.DEBUG:
				self.userID = 'AndromedaTestUserID'
			self.baseUrl = "www.yikyakapp.com"
			self.userAgent = 'android-async-http/1.4.4 (http://loopj.com/android-async-http)'
			self.longitude = 0
			self.latitude = 0
			self.handle = ''
			try:
				dbscream.BuildTables()
			except OperationalError:
				print("Tables already built")
					
		def newLocation(self):
			print("Do you have the latitude and logitude of your target location already(y/n)?")
			choice = raw_input("#: ")
			if choice not in ('y', 'n'):
				print("You entered an invalid option! Please try again!")
				self.__init__()
			if choice.lower().rstrip() == 'y':
				print("Please enter the latitude")
				self.latitude = raw_input("Latitude:  ")
				print("Please enter the longitude")
				self.longitude = raw_input("Longitude: ")
			else:
				print("Grabs street info in format:")
				print("<Street Number> <Street Name>, <Street Type>, <City>, <State>")
				print("Example: 1000 Mohegane Lake, Road, West Point, NY")
				print("It's important to get this right. Otherwise you won't get the right lat/long.")
				print("Street Number: ")
				self.streetNumber = raw_input("#: ")
				print("Street Name: ")
				self.streetName = raw_input("#: ")
				try:
					if self.streetName != '':
						self.streetName = '+'.join(self.streetName.split(' '))
				except:
					print("An error occurred in splitting streetName")
				print("Street Type: ")
				self.streetType = raw_input("#: ")
				try:
					if self.streetType != '':
						self.streetType = '+'.join(self.streetType.split(' '))
				except:
					print("An error occurred in splitting streetType")
				print("City: ")
				self.City = raw_input("#: ")
				try:
					if self.City != '':
						self.City = '+'.join(self.City.split(' '))
				except:
					print("An error occurred in splitting City")
				print("State: ")
				self.State = raw_input("#: ")
				if (len(self.State.rstrip()) > 2):
					print("The state should use 2-letter abbreviations")
					

				self.locRequestURL = \
				"https://maps.googleapis.com/maps/api/geocode/xml?address="\
				+self.streetNumber+'+'+self.streetName+'+'+self.streetType+'+'+self.City+'+'+self.State+'&sensor=false'
				print self.locRequestURL
				with open('data.xml', 'w') as xmldata:
					response = urllib2.urlopen(self.locRequestURL)
					page = response.read()
					xmldata.write(page)
				tempStore = xmlHandler.XMLResult('data.xml')
				self.latitude = tempStore.lat
				self.longitude= tempStore.lng
				host = 'www.yikyakapp.com'
    			url = '/YikYakFiles/updateLocation.php'
    			headers = {'User-Agent': self.userAgent,'Content-Type': 'application/x-www-form-urlencoded'}
    			values = {'lat': self.latitude, 'long' : self.longitude, 'userID': self.userID }
    			values = urllib.urlencode(values)
    			url = url + '?' + values
    			print(url)
    			conn = httplib.HTTPConnection(self.baseUrl)
    			conn.request("GET", url, "",  headers)
    			response = conn.getresponse()
    			data = response.read()
    			self.registerHandle()
    			print("Please enter a locname identifier for this location (Ex. WESTPOINT0)")
    			self.locname = raw_input("#: ")
    			dbscream.commitSessionChanges(self)
    			if self.DEBUG:
    				print(data)
    			self.main(self)

		def registerHandle(self, menu=False):
			print("Please enter a handle")
			self.handle = raw_input("#: ")
			headers = {'User-Agent': self.userAgent, 'Connection' : 'Keep-Alive', 'Content-Type': 'application/x-www-form-urlencoded'}
			values = {'userID': self.userID, 'handle' : self.handle}
			url = '/YikYakFiles/updateHandle.php'
			values = urllib.urlencode(values)
			url = url + '?' + values
			conn = httplib.HTTPConnection(self.baseUrl)
			conn.request("GET", url, None, headers)
			response = conn.getresponse()
			data = response.read()
			#print(data)
			dbscream.AddHandle(self)
			if menu:
				self.main(session)
			

		def getHandleInfo(self):
			headers = {'User-Agent': self.userAgent, 'Connection' : 'Keep-Alive', 'Content-Type': 'application/x-www-form-urlencoded'}
			values = {'userID': self.userID}
			url = '/YikYakFiles/getHandleInfo.php'
			values = urllib.urlencode(values)
			url = url + '?' + values
			conn = httplib.HTTPConnection(self.baseUrl)
			conn.request("GET", url, None, headers)
			response = conn.getresponse()
			data = response.read()
			#print(data)
			self.main(self)


		def generateNewUserID(self):
			headers = {'User-Agent': self.userAgent,'Content-Type': 'application/x-www-form-urlencoded'}
	   		url = '/YikYakFiles/registerUserDroid.php'
	   		conn = httplib.HTTPConnection(self.baseUrl)
	   		conn.request("GET", url, None,  headers)
	   		response = conn.getresponse()
	   		data = response.read()
			#print('Response: ', response.status, response.reason)
			#print('Data:')
			#print(data)
			self.userID = data
			self.newLocation()

		def loadPreviousSession(self):
			infoToLoad = dbscream.loadPreviousSessions()
			if not infoToLoad:
				print("Something went wrong in loading previous session!")
				self.main(self)
			else:
				try:
					self.userID = infoToLoad[0]
					self.longitude = infoToLoad[1]
					self.latitude = infoToLoad[2]
					self.handle = infoToLoad[3]
					self.locname = infoToLoad[4]
				except KeyError, TypeError:
					print("Something went wrong with their plans.")
			self.main(self)

		def getAreaTops(self):
			url = '/YikYakFiles/getAreaTops.php'
			# Yik Yak is picky about the http headers
			headers = {'Host' : self.baseUrl,'Connection' : 'Keep-Alive','User-Agent': self.userAgent}
			values = {'lat': self.latitude, 'long' : self.longitude}
			values = urllib.urlencode(values)
			#print values # you might want to check this to make sure it looks the way you want
			url = url + '?' + values
			#print url  # you might want to check this to make sure it looks the way you want
			conn = httplib.HTTPConnection(self.baseUrl)
			conn.request("GET", url, "", headers)
			response = conn.getresponse()
			data = response.read()
			data = json.loads(data)['messages']
			print('-'*20)
			for item in data:
				print("Message ID: " + str(item['messageID']) + '\t' + '#Likes: ' + str(item['numberOfLikes'] + '\t' +'Message: ' + item['message'] ))
			print('-'*20)
			print("\n\n")
			conn.close()
			self.main(self)
		
		def getAreaYaks(self, userID =''):
			url = '/YikYakFiles/getMessages.php'
			# Yik Yak is picky about the http headers
			headers = {'Host' : self.baseUrl,'Connection' : 'Keep-Alive','User-Agent': self.userAgent}
			if not userID:
				values = {'userID': self.userID }
				#print values
			else:
				values = {'userID' : unicode(userID) }
				#print values
			values = urllib.urlencode(values)
			#print values # you might want to check this to make sure it looks the way you want
			url = url + '?' + values
			#print url  # you might want to check this to make sure it looks the way you want
			conn = httplib.HTTPSConnection(self.baseUrl)
			conn.request("GET", url, "", headers)
			response = conn.getresponse()
			data = response.read()
			conn.close()
			return data

		def getPeekLocations(self):
			url = '/YikYakFiles/getPeekLocations.php'
			headers = {'User-Agent' : self.userAgent, 'Connection' : 'Keep-Alive', 'Content-Type' : 'application/x-www-form-urlencoded'}
			values = {'userID' : self.userID }
			values = urllib.urlencode(values)
			conn = httplib.HTTPSConnection(self.baseUrl)
			conn.request("GET", url, values, headers)
			response = conn.getresponse()
			data = response.read()
			data = json.loads(data)
			print('-'*20)
			for item in data['featuredLocations']:
				print("Latitude: " + str(item['latitude']) + '\t' + '#Longitude: ' + str(item['longitude'] + '\t' +'Location: ' + item['location'] ))
			print('-'*20)
			for item in data['otherLocations']:
				print("Latitude: " + str(item['latitude']) + '\t' + '#Longitude: ' + str(item['longitude'] + '\t' +'Location: ' + item['location'] ))
			print('-'*20)
			conn.close()
			self.main(self)

		def postYak(self):
			url = '/YikYakFiles/sendMessage.php'
			headers = {'User-Agent':self.userAgent, 'Connection' : 'Keep-Alive', 'Content-Type' : 'application/x-www-form-urlencoded'}
			print("Please enter a message to send")
			message = raw_input("#: ").rstrip()
			if not self.handle:
				values = { 'hidePin' : '1', 'lat' : self.latitude, 'long' : self.longitude, 'message' : message, 'userID' : self.userID}
			else:
				values = { 'hidePin' : '1', 'hndl' : self.handle, 'lat' : self.latitude, 'long' : self.longitude, 'message' : message, 'userID' : self.userID}
			values = urllib.urlencode(values)
			conn = httplib.HTTPSConnection(self.baseUrl)
			conn.request("POST", url, values, headers)
			response = conn.getresponse()
			data = response.read()
			print(data)
			conn.close()

		def showSessionInfo(self):
			print("Session Name: ", self.locname)
			print("UserID: ", self.userID)
			print("Latitude: ", self.latitude)
			print("Longitude: ", self.longitude)
			print("Handle: ", self.handle)
			self.main(self)