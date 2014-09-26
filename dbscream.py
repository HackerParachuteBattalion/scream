import sqlite3 as sl
import os
DEBUG = False

db = sl.connect("hacktheyak.db")
db.text_factory = str
dc = db.cursor()

def BuildTables():
	print "Attempting to creating tables..."
	dc.execute("CREATE TABLE SESSIONS(ID TEXT, LONG TEXT, LAT TEXT, HANDLE TEXT, LOCNAME TEXT)")
	dc.execute("CREATE TABLE UTA(ID TEXT)")
	dc.execute("CREATE TABLE DTA(ID TEXT)")
	dc.execute("CREATE TABLE PREVLOCNAME(ID TEXT, LOCNAME TEXT)")
	toInsert = ('only', 'none',)
	dc.execute("INSERT INTO PREVLOCNAME VALUES(?,?)", toInsert)
	db.commit()
def getPrevLocName():
	dc.execute("SELECT * FROM PREVLOCNAME")
	one = dc.fetchone()[1]
	if DEBUG:
		print one
	return one

def updatePrevLocName(loc):
	dc.execute("UPDATE PREVLOCNAME SET LOCNAME=? WHERE ID=?", (loc, 'only',))
	db.commit()

def AddHandle(session):
	dc.execute("UPDATE SESSIONS SET HANDLE=? WHERE ID=?", (session.handle, session.userID))

def AddUThrowAwayID(uid):
	toInsert = (uid,)
	dc.execute("INSERT INTO UTA VALUES(?)", toInsert)
	db.commit()

def AddDThrowAwayID(uid):
	toInsert = (uid,)
	dc.execute("INSERT INTO DTA VALUES(?)", toInsert)
	db.commit()

def commitSessionChanges(session):
	toInsert = (session.userID, str(session.longitude), str(session.latitude),str(session.handle), session.locname,)
	dc.execute("INSERT INTO SESSIONS VALUES(?,?,?,?,?)", toInsert)
	db.commit()

def checkNumUThrowAways(numVotes):
	num = len([row for row in dc.execute("SELECT * FROM UTA")])
	if num >= numVotes:
		return True
	else:
		return False

def checkNumDThrowAways(numVotes):
	num = len([row for row in dc.execute("SELECT * FROM DTA")])
	if num >= numVotes:
		return True
	else:
		return False

def getUThrowAways():
	throwAways = [row[0] for row in dc.execute("SELECT * FROM UTA")]
	return throwAways

def getDThrowAways():
	throwAways = [row[0] for row in dc.execute("SELECT * FROM DTA")]
	return throwAways

def loadPreviousSessions():
	print("Are you sure you want to load prevoius session(y/n)?")
	print("NOTE: This will overwrite the location you currently have set!")
	choice = raw_input("#: ")
	if choice.lower().rstrip() not in ('y' 'n'):
		print("Invalid choice selected!")
		print("Please try again!")
		displayPreviousSessions()
	elif choice.lower().rstrip() == 'y':
		for row in dc.execute("SELECT * FROM SESSIONS"):
			print(row)
		print("Please enter locname of requested session")
		locNameToGrab = raw_input("#: ")
		toGrab = (locNameToGrab,)
		dc.execute("SELECT * FROM SESSIONS WHERE LOCNAME=?", toGrab)
		return dc.fetchone()	
	else:
		print("OK!")
		return

def displayUThrowAways():
	for row in dc.execute("SELECT * FROM UTA"):
		print row[0]

def displayDThrowAways():
	for row in dc.execute("SELECT * FROM DTA"):
		print row[0]

def displayPreviousSessions():
	if DEBUG:
		print "call"
	for row in dc.execute("SELECT * FROM SESSIONS"):
		if DEBUG:
			print(type(row))
		print(row)
	print("If there are no previous sessions, then you will only see this sentence.\n\n")
