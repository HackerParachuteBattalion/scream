import session, dbscream, json
from votebomb import VoteBomb
try:
	#GLOBALS#
	DEBUG = False
	
	def main(session):
		'''Print Basic Menu'''
		print("1. Generate new userID")
		print("2. Set/Change Location")
		print("3. Get Peek Locations")
		print("4. Display Previous Sessions")
		print("5. Load Previous Session")
		print("6. Grab hottest yaks for area")
		print("7. Grab all yaks for area")
		print("8. Display all throw away IDs")
		print("9. Up/Down Vote Bomb")
		print("10. Post a Yak")
		print("11. Show session information")
		print("12. Get Handle Info")
		print("13. Set Handle")
		print("14. Exit")
		if DEBUG:
			print("#Testing Menu Below:")
			print("--|A. ")
			print("--|D. Get Peek Locations")
		choice = raw_input("#: ")
		if choice == '1':
			session.generateNewUserID()
			main(session)
		elif choice == '2':
			session.newLocation()
		elif choice =='3':
			session.getPeekLocations()
		elif choice == '4':
			print("===Up-Vote Throw Away Ids===")
			dbscream.displayUThrowAways()
			print("===Down-Vote Throw Away Ids===")
			dbscream.displayDThrowAways()
			main(session)
		elif choice == '5':
			session.loadPreviousSession()
		elif choice == '6':
			session.getAreaTops()
		elif choice == '7':
			data = session.getAreaYaks()
			data = json.loads(data)['messages']
			print('-'*20)
			for item in data:
				print("Message ID: " + str(item['messageID']) + '\t' + '#Likes: ' + str(item['numberOfLikes'] + '\t' +'Message: ' + item['message'] ))
			print('-'*20)
			print("\n\n")
			main(session)
		elif choice == '8':
			dbscream.displayUThrowAways()
			dbscream.displayDThrowAways()
			print("\n\n")
			main(session)
		elif choice == '9':
			vb = VoteBomb(session, DEBUG)
			main(session)
		elif choice == '10':
			session.postYak()
			main(session)
		elif choice == '11':
			try:
				session.showSessionInfo()
			except AttributeError:
				print("It seems your information is not yet set!")
				print("Please choose another option!")
				main(session)
		elif choice == '12':
			session.getHandleInfo()
		elif choice == '13':
			session.registerHandle(menu=True)
		elif choice == '14':
			exit()


		if DEBUG:
			if choice.lower().rstrip() == 'a':
				'''Insert functionality to test here'''
				data = session.getAreaYaks(userID=str("c090c991-d7fc-11e3-a6c0-0401130aa601"))
				data = json.loads(data)['messages']
				print('-'*20)
				for item in data:
					print("Message ID: " + str(item['messageID']) + '\t' + '#Likes: ' + str(item['numberOfLikes'] + '\t' +'Message: ' + item['message'] ))
				print('-'*20)
				#data = session.getAreaYaks(userID=str("59b9e8cb-d78f-11e3-a6c0-0401130aa601"))
				#data = json.loads(data)['messages']
				#print('-'*20)
				#for item in data:
			#		print("Message ID: " + str(item['messageID']) + '\t' + '#Likes: ' + str(item['numberOfLikes'] + '\t' +'Message: ' + item['message'] ))
				#print('-'*20)


	if __name__ == "__main__":
		session = session.Session(main, DEBUG)
		main(session)



except KeyboardInterrupt:
	import this
