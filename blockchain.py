#!/usr/bin/env python3
from Node import Node
from LinkedList import LinkedList
import sys
import getopt
from datetime import datetime

def arginit(argv):
	i = 2
	itemIDs = []
	if argv[1] == "add":
		add_ll = LinkedList()
		if len(argv) > 2:
			if argv[i] == "-c":
				caseID = argv[i+1]
				print("Case: " + caseID)
				i = i+2
				numitems = 0
				while i < len(argv):
					if argv[i] == "-i":
						#evidenceID should be i+1
						#add() should handle all the prints necessary for each evidenceID provided & does the check for the evidenceID existing in LL
						add_ll.add(caseID, i+1)
						#itemIDs.append(argv[i+1])
						#print("Added item: " + itemIDs[numitems])
						#numitems = numitems+1
						#TO DO: Add caseID, itemID to blockchain Node, establish Node
						#print(" Status: ")
						#print(" Time of action: ")
					else:
						exit(3)
					i = i+2
					
			else:
				exit(3)
		else:
			exit(3)	
	elif argv[1] == "checkout":
		checkout_ll = LinkedList()
		if len(argv) > 2:
			if argv[i] == "-i":
				evidenceID = argv[i+1]
				#checkout() handles all the prints & error checking
				#TO CHECK: should we be throwing the exit(1) from the LinkedList class instead of returing False?
				checkout_ll.checkout(evidenceID)
				#checkedOut = False
				#Fetch caseID of block with matching itemID and block info
				#print("Case: ")
				#if checkedOut == False:
				#	print("Checked out item: " + argv[i+1])
				#	print(" Status: ")
				#	print(" Time of action: ")
				#else:
				#	print("Error: Cannot check out a checked out item. Must check in first.")
				#	exit(1)
			else:
				exit(3)
		else:
			exit(3)
		
	elif argv[1] == "checkin":
		checkin_ll = LinkedList()
		if len(argv) > 2:
			if argv[i] == "-i":
				#Fetched evidenceID of block with matching itemID and block info
				evidenceID = argv[i+1]
				#checkin() handles all the prints & error checking
				#ALTHOUGH, I am unsure if previousHash refers to previous node in LL, which is the check if the evidenceID passed has already been added to blockchain
				checkin_ll.checkin(evidenceID)
				#print("Case: ")
				#print("Checked in item: " + argv[i+1])
				#print(" Status: ")
				#print(" Time of action: ")
			else:
				exit(3)
		else:
			exit(3)
	elif argv[1] == "log":
		log_ll = LinkedList()
		if len(argv) > 2:
			if argv[i] == "-r": # Reverse order of log entries printed. This will be newest to oldest.
			#Fetch caseID of block with matching itemID and block info
				log_ll.printLog()	
			#elif argv[i] == "-n": Set number of log entries
				count = i+1
				log_ll.log(None, count, None)
			#elif argv[i] == "-i": # Find log entries with matched itemID
				evidenceID = i+1
				log_ll.log(evidenceID, 0, None)
			#elif argv[i] == "-c": # Find log entries with matched caseID
				caseID = i+1
				log_ll.log(None, 0, caseID)
			
			#else: # Print all contents of the log. This will be in the oldest to newest changes
				log_ll.log(None, 0, None)
		else:
			exit(3)
	elif argv[1] == "remove":
		remove_ll = LinkedList()
		if len(argv) > 2:
			if argv[i] == "-i":
				evidenceID = 0 # set to blockchain node with matching itemID - need this to be grabbed from arguements so that remove() knows what it's looking for
				i = i+2
				if argv[i] == "-y":
					#remove() will print ther caseID, evidenceID, & new status, & handle the error check of it being checkin
					remove_ll.remove(evidenceID)
					#print("Case: ")
					#print("Removed item:" + argv[i-1])
					#print(" Status: ")
					i = i+2
					if argv[i] == "-o":
						print("\tOwner info: NEED TO IMPLEMENT TO TAKE OWNER INFO FROM ARGS & PLACE HERE")
					timeOfAction = datetime.now()
					iso_timeOfAction = datetime.isoformat(timeOfAction)
					print("\tTime of action: " + str(timeOfAction))
				else:
					exit(3)
					
			else:
				exit(3)
		else:
			exit(3)	
	elif argv[1] == "init":
		init_ll = LinkedList()
		#init() does all the checks 
		init_ll.init()
		#Check if head node is made.
		#nodeFound = False
		#if nodeFound == False:
		#	print("Blockchain file not found. Created INITIAL block.")
		#else:
		#	print("Blockchain file found with INITIAL block.")
			
	elif argv[1] == "verify":
		verify_ll = LinkedList()
		#Handles all the logic and print - NEED TO GRAB REASON WHY IT'S BAD BLOCK
		verify_ll.verify()

def main():
    arginit(sys.argv)
    

main()