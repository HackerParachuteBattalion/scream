import dbscream, json, hashlib, urllib, httplib

class VoteBomb():
		def __init__(self, session, DEBUG=False):
			self.needUThrowAways = True
			self.needDThrowAways = True
			self.DEBUG = DEBUG
			self.session = session
			self.ubombShell = dict()
			self.dbombShell = dict()
			self.messageToMatch = ''
			self.uvthrowAwayIDs = []
			self.dvthrowAwayIDs = []
			self.userAgent = 'android-async-http/1.4.4 (http://loopj.com/android-async-http)'
			self.latitude = session.latitude
			self.longitude = session.latitude
			self.currentLocName = session.locname
			print("How many votes would you like for a post?:\n")
			self.numVotes = raw_input("#: ")	
			if not self.numVotes.isdigit():
				print("You entered an invalid number.")
				print("Please try again!")
				self.__init__(session)
			else:
				self.numVotes = int(self.numVotes)
				if dbscream.checkNumUThrowAways(self.numVotes):
					self.needUThrowAways = False
				if dbscream.checkNumDThrowAways(self.numVotes):
					self.needDThrowAways = False

			print("Up-vote or down-vote (u/d)?:\n")
			self.uv = raw_input("#: ")
			if self.uv.lower().rstrip() not in ('u', 'd'):
				print("Invalid choice. Please try again.")
				self.__init__(session)
			else:
				self.initUThrowAways()
				self.initDThrowAways()
				#This may or may not work. Probably better to leave it commented out for now.
				#if self.currentLocName != dbscream.getPrevLocName():
				#	print("Updating location of stored userIDs\n\n")
				#	self.updateAllLocations()
				#	dbscream.updatePrevLocName(self.currentLocName)
				self.findUMessageIDs()
				self.launchNuke()

		def updateSingleLocation(self, uid):
			host = 'www.yikyakapp.com'
			url = '/YikYakFiles/updateLocation.php'
			headers = {'User-Agent': self.userAgent,'Content-Type': 'application/x-www-form-urlencoded'}
			values = {'userID': uid, 'lat': self.latitude, 'long' : self.longitude}
			values = urllib.urlencode(values)
			url = url + '?' + values
			if self.DEBUG:
				print(url)
			conn = httplib.HTTPSConnection(host)
			conn.request("GET", url, "",  headers)
			response = conn.getresponse()
			data = response.read()
			print data

		def updateAllLocations(self):
			for i in range(self.numVotes):
				self.updateSingleLocation(self.uvthrowAwayIDs[i])
			for i in range(self.numVotes):
				self.updateSingleLocation(self.dvthrowAwayIDs[i])

		def initUThrowAways(self):
			if self.needUThrowAways and self.uv == 'u':
				print("Generating Up-vote ThrowAways")
				for i in range(self.numVotes):
					self.uvthrowAwayIDs.append(self.generateThrowAwayUserID())
				if self.DEBUG:
					print(self.uvthrowAwayIDs)
				for uid in self.uvthrowAwayIDs:
					dbscream.AddUThrowAwayID(uid)
					if self.currentLocName != dbscream.getPrevLocName():
						print("Updating uUid Locations")
						self.updateLocation(uid)
				dbscream.updatePrevLocName(self.currentLocName)
			elif self.uv =='d':
				pass
			else:
				for uid in dbscream.getUThrowAways():
					self.uvthrowAwayIDs.append(uid)
				if self.currentLocName != dbscream.getPrevLocName():
					print("Updating uUid Locations")
					for uid in self.uvthrowAwayIDs:
						self.updateLocation(uid)
				dbscream.updatePrevLocName(self.currentLocName)


		def initDThrowAways(self):
			if self.needDThrowAways and self.uv =='d':
				print("Generating Down-vote ThrowAways")
				for i in range(self.numVotes):
					self.dvthrowAwayIDs.append(self.generateThrowAwayUserID())
				if self.DEBUG:
					print(self.dvthrowAwayIDs)
				for uid in self.dvthrowAwayIDs:
					dbscream.AddDThrowAwayID(uid)
					if self.currentLocName != dbscream.getPrevLocName():
						print("Updating dUid Locations")
						self.updateLocation(uid)
				dbscream.updatePrevLocName(self.currentLocName)
			elif self.uv == 'u':
				pass
			else:
				for uid in dbscream.getDThrowAways():
					self.dvthrowAwayIDs.append(uid)
				if self.currentLocName != dbscream.getPrevLocName():
					print("Updating dUid Locations")
					for uid in self.dvthrowAwayIDs:
						self.updateLocation(uid)
				dbscream.updatePrevLocName(self.currentLocName)


		def findUMessageIDs(self):
			data = self.session.getAreaYaks()
			data = json.loads(data)['messages']
			print('-'*20)
			for item in data:
				print("Message ID: " + str(item['messageID']) + '\t' + '#Likes: ' + str(item['numberOfLikes'] + '\t' +'Message: ' + item['message'] ))
			print('-'*20)
			print("Select a messageID from above to bomb")
			self.mid = raw_input("#: ")
			if not self.mid.isdigit():
				print("Invalid choice. Please try again!")
				self.findUMessageIDs()
			else:
				self.mid = int(self.mid)
			
			for item in data:
				if self.mid == item['messageID']:
					if self.DEBUG:
						print item['messageID']
					self.messageToMatch = item['message'].lower().rstrip().strip()
					if self.DEBUG:
						print "Mtm: %r" % self.messageToMatch
			if self.uv == 'u':
				if self.DEBUG:
					print self.uvthrowAwayIDs
				for i in range(self.numVotes):
					uid = self.uvthrowAwayIDs[i]
					if self.DEBUG:
						print uid
					data = self.session.getAreaYaks(userID=uid)
					data = json.loads(data)['messages']
					if self.DEBUG:
						print uid, data
					if self.DEBUG:
						print data
					for item in data:
						message = item['message'].lower().rstrip().strip()
						if self.messageToMatch == message:
							self.ubombShell[uid] = item['messageID']
							if self.DEBUG:
								print self.ubombShell[uid]
			elif self.uv == 'd':
				if self.DEBUG:
					print self.dvthrowAwayIDs
				for i in range(self.numVotes):
					uid = self.dvthrowAwayIDs[i]
					if self.DEBUG:
						print uid
					data = self.session.getAreaYaks(userID=uid)
					data = json.loads(data)['messages']
					if self.DEBUG:
						print uid #data
					if self.DEBUG:
						print data
					for item in data:
						message = item['message'].lower().rstrip().strip()
						if self.messageToMatch == message:
							self.dbombShell[uid] = item['messageID']
							if self.DEBUG:
								print self.dbombShell[uid]
		
		def launchNuke(self):
			if self.DEBUG:
				print self.ubombShell
				print self.dbombShell
			if self.uv == 'u':
				for i in range(self.numVotes):
					uid = self.uvthrowAwayIDs[i]
					self.upVoteMessage(uid, self.ubombShell[uid])
			elif self.uv == 'd':
				for i in range(self.numVotes):
					uid = self.dvthrowAwayIDs[i]
					self.downVoteMessage(uid, self.dbombShell[uid])

		def generateThrowAwayUserID(self):
			headers = {'User-Agent': self.session.userAgent,'Content-Type': 'application/x-www-form-urlencoded'}
	   		url = '/YikYakFiles/registerUserDroid.php'
	   		conn = httplib.HTTPConnection(self.session.baseUrl)
	   		conn.request("GET", url, None,  headers)
	   		response = conn.getresponse()
	   		data = response.read()
	   		conn.close()
	   		if self.DEBUG:
	   			print data
	   		return data

	   	def updateLocation(self, uid):
			host = 'www.yikyakapp.com'
			url = '/YikYakFiles/updateLocation.php'
			headers = {'User-Agent': self.session.userAgent,'Content-Type': 'application/x-www-form-urlencoded'}
			values = {'lat': self.session.latitude, 'long' : self.session.longitude, 'userID': uid }
			values = urllib.urlencode(values)
			url = url + '?' + values
			conn = httplib.HTTPSConnection(self.session.baseUrl)
			conn.request("GET", url, "",  headers)
			response = conn.getresponse()
			data = response.read()
			print(data)

		def upVoteMessage(self,userID, messageID):
			host = 'www.yikyakapp.com'
			url = '/YikYakFiles/likeMessage.php'
			headers = {'User-Agent': self.session.userAgent, 'Connection' : 'Keep-Alive', 'Content-Type': 'application/x-www-form-urlencoded'}
			values = {'messageID' : messageID, 'userID': userID}
			values = urllib.urlencode(values)
			url = url + '?' + values
			conn = httplib.HTTPConnection(host)
			conn.request("GET", url, "", headers)
			response = conn.getresponse()
			data = response.read()
			if self.DEBUG:
				print('Response: ', response.status, response.reason)
				print('Data:')
				print(data)
			conn.close()

		def downVoteMessage(self,userID, messageID):
			host = 'www.yikyakapp.com'
			url = '/YikYakFiles/downvoteMessage.php'
			headers = {'User-Agent': self.session.userAgent, 'Connection' : 'Keep-Alive', 'Content-Type': 'application/x-www-form-urlencoded'}
			values = {'messageID' : messageID, 'userID': userID}
			values = urllib.urlencode(values)
			url = url + '?' + values
			conn = httplib.HTTPConnection(host)
			conn.request("GET", url, "", headers)
			response = conn.getresponse()
			data = response.read()
			if self.DEBUG:
				print('Response: ', response.status, response.reason)
				print('Data:')
				print(data)
			conn.close()