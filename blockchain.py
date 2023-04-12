#!/usr/bin/env python3
import sys
import getopt
import hashlib
import collections
import struct
import os
from datetime import datetime
import time

block_layout = struct.Struct(b'32s d 16s I 12s I') # Layout of first six block values
block_datainit_layout = struct.Struct(b'14s ') # Layout of block data for the inital block
block_data_layout = struct.Struct('0s ') # Layout of block data for added blocks
BC_STATS = collections.namedtuple('BC_STATS', ['Previous_Hash', 'Timestamp', 'Case_ID', 'Evidence_Item_ID', 'State', 'Data_Length']) # Variables stored in first six block values
BC_DATA = collections.namedtuple('BC_DATA', ['Data']) # Data variable for block
bc_list = collections.namedtuple('bc_list', ['Case','ID', 'Status', 'Time']) # Layout for list (unused)
bc_checkout = collections.namedtuple('bc_checkout', ['ID', 'Status']) # Layout for checkedout item

	
def arginit(argv):
#Set BCHOC environment variable (local file bchocout for blockchain or file path defined by gradescope)
	key = 'BCHOC_FILE_PATH'
	if key in os.environ:
		filePath = os.environ[key]
	else:
		filePath = "bchocout"
	logPath = "logfile.txt"
	i = 2
	itemIDs = [] #array to track the evidence ID's, makes checking easier
	if (len(argv) == 1): # No arugments to the program, abort
		exit(3)
	if argv[1] == "add":
		blockStat = [] # Array storing the blocks read from the blockchain
		if len(argv) > 2:
			if argv[i] == "-c": # Case ID
				caseID = argv[i+1] #saves Case ID
				i = i+2
				numitems = -1
				if i >= len(argv):
					print("No evidence ID given, aborted.")
					exit(1) # No evidence id given, not possible
				while i < len(argv): #For each item ID, check to see if it should be added
					if argv[i] == "-i":
						itemFound = False
						itemIDs.append(argv[i+1])
						numitems = numitems+1
						#Check if evidence id exists in chain, if it does, do not add
						try:
							with open(filePath, 'rb') as fileRead:
								initOnly = True # Blockchain only contains an init block.
								numblocks = -1
								bcstatsinit = fileRead.read(block_layout.size) # Read inital block first 6 values
								#bcstatsinit = BC_STATS._make(block_layout.unpack(bcstatsinit))
								bcdatainit = fileRead.read(block_datainit_layout.size) # Read inital block data
								#bcdatainit = BC_DATA._make(block_datainit_layout.unpack(bcdatainit))
								while True: # Read all blocks in the blockchain to see if the evidenceID already exists in the chain.
									bcstats = fileRead.read(block_layout.size)
									if not bcstats: # if at the end of the file, bcstats is overwritten, so change value back to the last block stats
										if numblocks != -1: # If there is more than the inital block in the chain, set bcstats to the previous block values to calculate the previous hash.
											bcstats = blockStat[numblocks]
										fileRead.close()
										break
									numblocks = numblocks+1
									initOnly = False
									bcstatsm = BC_STATS._make(block_layout.unpack(bcstats))
									dataRead = fileRead.read(bcstatsm.Data_Length) #read's all the data based on date_length size; mostly for remove since they are the blocks with varying data length
									blockStat.append(bcstats)
									evidence = bcstatsm.Evidence_Item_ID
									if str(evidence) == itemIDs[numitems]: #The evidenceID is found in the blockchain.
										itemFound = True
						except FileNotFoundError as e: # Adding to a file that doesn't exist, create the initial block.
								fileWrite = open(filePath, 'wb')
								inits = BC_STATS(str.encode(""), 0, str.encode(""), 0, str.encode("INITIAL"), 14)
								initd = BC_DATA(str.encode("Initial block"))
								inits = block_layout.pack(*inits)
								initd = block_datainit_layout.pack(*initd)
								fileWrite.write(inits)
								fileWrite.write(initd)
								fileWrite.close()
								fileWrite = open(logPath, 'w') # Add action to logfile.
								caseID = "00000000-0000-0000-0000-000000000000"
								itemID = "0"
								reason = "INITIAL"
								currTime = datetime.utcnow()
								fileWrite.write(caseID + "\n")
								fileWrite.write(itemID + "\n")
								fileWrite.write(reason + "\n")
								fileWrite.write(currTime.strftime("%Y-%m-%dT%H:%M:%S.%fZ") + "\n")
								fileWrite.close()
								print("Blockchain file not found. Created INITIAL block.")
								exit(0)
						#If the evidence item doesn't exist, peform the hash of the last item in the chain and append to the file
						if itemFound == False:
							if caseID[8] != "-": # Standardize caseID format for prining and remove dashes for storage in the blockchain
								newcaseID = caseID[:8]+'-'+caseID[8:12]+'-'+caseID[12:16]+'-'+caseID[16:20]+'-'+caseID[20:]
								print("Case: " + newcaseID)
								caseBytes = bytearray.fromhex(caseID) 
								caseBytes.reverse()
								print(caseBytes)
							else:
								newcaseID = caseID
								caseID = caseID.replace('-', '')
								caseBytes = bytearray.fromhex(caseID)
								caseBytes.reverse()
								print(caseBytes)
								print("Case: " + newcaseID)
							print("Added item: " + itemIDs[numitems])
							print("\tStatus: CHECKEDIN")
							currTime = datetime.utcnow()
							print("\tTime of action: " + currTime.strftime("%Y-%m-%dT%H:%M:%S.%fZ"))
							fileWrite = open(logPath, 'a') # Add action to logfile.
							fileWrite.write(newcaseID + "\n")
							fileWrite.write(itemIDs[numitems] + "\n")
							fileWrite.write("CHECKEDIN" + "\n")
							fileWrite.write(currTime.strftime("%Y-%m-%dT%H:%M:%S.%fZ") + "\n")
							fileWrite.close()
							if initOnly == True: # Blockchain with only the inital file, add the block to the second position in the file.
								fileWrite = open(filePath, 'ab') #APPEND to bc file, must use 'ab'
								secondst = BC_STATS(str.encode(""), datetime.timestamp(currTime), caseBytes, int(itemIDs[numitems]), str.encode("CHECKEDIN"), 0)
								secondst = block_layout.pack(*secondst)
								print(secondst) # For debugging
								fileWrite.write(secondst)
								fileWrite.close()
							else: # Blockchain with several blocks, find the hash of the last stored node and add the user's block to the end of the file.
								block256 = hashlib.sha256()
								
								block256.update(bcstats)
								fileWrite = open(filePath, 'ab') #APPEND to bc file, must use 'ab'

								blockst = BC_STATS(str.encode(block256.hexdigest()), datetime.timestamp(currTime), caseBytes, int(itemIDs[numitems]), str.encode("CHECKEDIN"), 0)
								blockst = block_layout.pack(*blockst)
								print(blockst) # For debugging
								fileWrite.write(blockst)
								fileWrite.close()
						else: # If the item was found in the chain, do nothing.
							print("Trying to add duplicate block, aborted.")
							exit(1)
							
					else: # Invalid argument layout
						exit(1)
					i = i+2
					
			else: # Invalid argument layout
				exit(1)
		else: # Invalid argument layout
			exit(1)	
			
	elif argv[1] == "checkout":
		if len(argv) > 2:
			if argv[i] == "-i":
				checkedOut = False
				itemID = argv[i+1]
				i = 0
				caseID = "0"
				blockStat = []
				try:
					with open(filePath, 'rb') as fileRead:
						initOnly = True # Blockchain only contains an init block.
						numblocks = -1
						bcstatsinit = fileRead.read(block_layout.size) # Read inital block first 6 values
						#bcstatsinit = BC_STATS._make(block_layout.unpack(bcstatsinit))
						bcdatainit = fileRead.read(block_datainit_layout.size) # Read inital block data
						#bcdatainit = BC_DATA._make(block_datainit_layout.unpack(bcdatainit))
						while True: # Read all blocks in the blockchain to see if the evidenceID already exists in the chain.
							bcstats = fileRead.read(block_layout.size)
							if not bcstats: # if at the end of the file, bcstats is overwritten, so change value back to the last block stats
								if numblocks != -1: # If there is more than the inital block in the chain, set bcstats to the previous block values to calculate the previous hash.
									bcstats = blockStat[numblocks]
								fileRead.close()
								break
							numblocks = numblocks+1
							initOnly = False
							bcstatsm = BC_STATS._make(block_layout.unpack(bcstats))
							dataRead = fileRead.read(bcstatsm.Data_Length) #read's all the data based on date_length size; mostly for remove since they are the blocks with varying data length
							blockStat.append(bcstats)
							evidence = bcstatsm.Evidence_Item_ID
				except FileNotFoundError as e: # Adding to a file that doesn't exist, create the initial block.
						fileWrite = open(filePath, 'wb')
						inits = BC_STATS(str.encode(""), 0, str.encode(""), 0, str.encode("INITIAL"), 14)
						initd = BC_DATA(str.encode("Initial block"))
						inits = block_layout.pack(*inits)
						initd = block_datainit_layout.pack(*initd)
						fileWrite.write(inits)
						fileWrite.write(initd)
						fileWrite.close()
						fileWrite = open(logPath, 'w') # Add action to logfile.
						caseID = "00000000-0000-0000-0000-000000000000"
						itemID = "0"
						reason = "INITIAL"
						currTime = datetime.utcnow()
						fileWrite.write(caseID + "\n")
						fileWrite.write(itemID + "\n")
						fileWrite.write(reason + "\n")
						fileWrite.write(currTime.strftime("%Y-%m-%dT%H:%M:%S.%fZ") + "\n")
						fileWrite.close()
						print("Blockchain file not found. Created INITIAL block.")
						exit(0)
				#Fetch caseID of block with matching itemID and block info
				with open(logPath, 'r') as fileRead:
					itemFound = False
					invalid = False
					content = fileRead.readlines()
					content = [x.strip() for x in content]
					j = 0
					while j < len(content):
						if content[j] == itemID:
							itemFound = True
							caseID = content[j-1]
							if caseID[8] != "-": # Standardize caseID format for prining and remove dashes for storage in the blockchain
								newcaseID = caseID[:8]+'-'+caseID[8:12]+'-'+caseID[12:16]+'-'+caseID[16:20]+'-'+caseID[20:]
								print("Case: " + newcaseID)
								caseBytes = bytearray.fromhex(caseID) 
								caseBytes.reverse()
							else:
								newcaseID = caseID
								caseID = caseID.replace('-', '')
								caseBytes = bytearray.fromhex(caseID)
								caseBytes.reverse()
							if content[j+1] == "CHECKEDOUT":
								checkedOut = True
							elif content[j+1] == "CHECKEDIN":
								checkedOut = False
							elif content[j+1] == "DISPOSED" or content[j+1] == "DESTROYED" or content[j+1] == "RELEASED":
								invalid = True
						j = j+1
				if invalid == False:
					if itemFound == True:
						if checkedOut == False:
							print("Case: " + newcaseID)
							print("Checked out item: " + itemID)
							print("\tStatus: CHECKEDOUT")
							currTime = datetime.utcnow()
							print("\tTime of action: " + currTime.strftime("%Y-%m-%dT%H:%M:%S.%fZ"))
							fileWrite = open(logPath, 'a') # Add action to logfile.
							fileWrite.write(newcaseID + "\n")
							fileWrite.write(itemID + "\n")
							fileWrite.write("CHECKEDOUT" + "\n")
							fileWrite.write(currTime.strftime("%Y-%m-%dT%H:%M:%S.%fZ") + "\n")
							fileWrite.close()
							#adding to blockchain file.
							block256 = hashlib.sha256()
							block256.update(bcstats)
							fileWrite = open(filePath, 'ab') #APPEND to bc file, must use 'ab'
							blockst = BC_STATS(str.encode(block256.hexdigest()), datetime.timestamp(currTime), caseBytes, int(itemID), str.encode("CHECKEDOUT"), 0)
							blockst = block_layout.pack(*blockst)
							fileWrite.write(blockst)
							fileWrite.close()	
						else:
							print("Error: Cannot check out a checked out item. Must check in first.")
							exit(1)
					else:
						print("Error: Cannot check out an item that has not been added. Must add it in first.")
						exit(1)
				else:
					print("Error: Invalid status on block, therefore cannot check out.")
					exit(1)
			else:
				exit(1)
		else:
			exit(1)
		
	elif argv[1] == "checkin":
		if len(argv) > 2:
			checkedIn = False
			itemID = argv[i+1]
			caseID = "0"
			blockStat = []
			try:
				with open(filePath, 'rb') as fileRead:
					initOnly = True # Blockchain only contains an init block.
					numblocks = -1
					bcstatsinit = fileRead.read(block_layout.size) # Read inital block first 6 values
					#bcstatsinit = BC_STATS._make(block_layout.unpack(bcstatsinit))
					bcdatainit = fileRead.read(block_datainit_layout.size) # Read inital block data
					#bcdatainit = BC_DATA._make(block_datainit_layout.unpack(bcdatainit))
					while True: # Read all blocks in the blockchain to see if the evidenceID already exists in the chain.
						bcstats = fileRead.read(block_layout.size)
						print(bcstats)
						if not bcstats: # if at the end of the file, bcstats is overwritten, so change value back to the last block stats
							if numblocks != -1: # If there is more than the inital block in the chain, set bcstats to the previous block values to calculate the previous hash.
								bcstats = blockStat[numblocks]
							fileRead.close()
							break
						numblocks = numblocks+1
						initOnly = False
						bcstatsm = BC_STATS._make(block_layout.unpack(bcstats))
						dataRead = fileRead.read(bcstatsm.Data_Length) #read's all the data based on date_length size; mostly for remove since they are the blocks with varying data length
						blockStat.append(bcstats)
						evidence = bcstatsm.Evidence_Item_ID
			except FileNotFoundError as e: # Adding to a file that doesn't exist, create the initial block.
					fileWrite = open(filePath, 'wb')
					inits = BC_STATS(str.encode(""), 0, str.encode(""), 0, str.encode("INITIAL"), 14)
					initd = BC_DATA(str.encode("Initial block"))
					inits = block_layout.pack(*inits)
					initd = block_datainit_layout.pack(*initd)
					fileWrite.write(inits)
					fileWrite.write(initd)
					fileWrite.close()
					fileWrite = open(logPath, 'w') # Add action to logfile.
					caseID = "00000000-0000-0000-0000-000000000000"
					itemID = "0"
					reason = "INITIAL"
					currTime = datetime.utcnow()
					fileWrite.write(caseID + "\n")
					fileWrite.write(itemID + "\n")
					fileWrite.write(reason + "\n")
					fileWrite.write(currTime.strftime("%Y-%m-%dT%H:%M:%S.%fZ") + "\n")
					fileWrite.close()
					print("Blockchain file not found. Created INITIAL block.")
					exit(0)
			#Fetch caseID of block with matching itemID and block info
			with open(logPath, 'r') as fileRead:
				itemFound = False
				invalid = False
				content = fileRead.readlines()
				content = [x.strip() for x in content]
				j=0
				while j < len(content):
					if content[j] == itemID:
						itemFound = True
						caseID = content[j-1]
						if caseID[8] != "-": # Standardize caseID format for prining and remove dashes for storage in the blockchain
							newcaseID = caseID[:8]+'-'+caseID[8:12]+'-'+caseID[12:16]+'-'+caseID[16:20]+'-'+caseID[20:]
							print("Case: " + newcaseID)
							caseBytes = bytearray.fromhex(caseID) 
							caseBytes.reverse()
						else:
							newcaseID = caseID
							caseID = caseID.replace('-', '')
							caseBytes = bytearray.fromhex(caseID)
							caseBytes.reverse()
						if content[j+1] == "CHECKEDIN":
							checkedIn = True
						elif content[j+1] == "CHECKEDOUT":
							checkedIn = False
						elif content[j+1] == "DISPOSED" or content[j+1] == "DESTROYED" or content[j+1] == "RELEASED":
							invalid = True
					j = j+1
				if invalid == False:
					if itemFound == True:
						if checkedIn == False:
							print("Case: " + caseID)
							print("Checked in item: " + itemID)
							print("\tStatus: CHECKEDIN")
							currTime = datetime.utcnow()
							print("\tTime of action: " + currTime.strftime("%Y-%m-%dT%H:%M:%S.%fZ"))
							fileWrite = open(logPath, 'a') # Add action to logfile.
							fileWrite.write(newcaseID + "\n")
							fileWrite.write(itemID + "\n")
							fileWrite.write("CHECKEDIN" + "\n")
							fileWrite.write(currTime.strftime("%Y-%m-%dT%H:%M:%S.%fZ") + "\n")
							fileWrite.close()
							#adding to blockchain file
							block256 = hashlib.sha256()
							block256.update(bcstats)
							fileWrite = open(filePath, 'ab') #APPEND to bc file, must use 'ab'
							blockst = BC_STATS(str.encode(block256.hexdigest()), datetime.timestamp(currTime), caseBytes, int(itemID), str.encode("CHECKEDIN"), 0)
							blockst = block_layout.pack(*blockst)
							fileWrite.write(blockst)
							fileWrite.close()	
						else:
							print("Error: Cannot check in a checked in item.")
							exit(1)
					else:
						print("Error: Cannot check in an item that has not been added. Must add it in first.")
						exit(1)
				else:
					print("Error: Invalid status on block, therefore cannot check out.")
					exit(1)
		else:
			exit(1)
			
	elif argv[1] == "log":
		reverse = False
		case = False
		caseID = 0
		item = False
		itemID = 0
		number = False
		num_entries = 0
		logPrint = []
		if len(argv) > 2:
			i = 2
			increase = 0
			while i < len(argv):
				#print(argv[i])
				#print(i)
				if argv[i] == "-r" or argv[i] == "--reverse":
					reverse = True
					i = i+1
					continue
				if argv[i] == "-c":
					case = True
					caseID = argv[i+1]
					i = i+2
					continue
				if argv[i] == "-i":
					item = True
					itemID = argv[i+1]
					i = i+2
					continue
				if argv[i] == "-n":
					number = True
					num_entries = int(argv[i+1])*4
					if (num_entries < 0):
						num_entries = 999
					i = i+2
					continue
			#print(reverse)
			#print(case)
			#print(item)
			#print(number)
		elif len(argv) == 2: # Print entire log
			with open(logPath, 'r') as fileRead:
				content = fileRead.readlines()
				content = [x.strip() for x in content]
				i = 0
				while i < len(content):
					print("Case: " + content[i])
					print("Item: " + content[i+1])
					print("Action: " + content[i+2])
					print("Time: " + content[i+3])
					print("")
					i = i+4
			exit(0)
		if reverse == True:
			if case == True:
				with open(logPath, 'r') as fileRead:
					content = fileRead.readlines()
					content = [x.strip() for x in content]	
				i = len(content)-4
				while i >= 0: # Build an array of all log entries with matching caseID in reverse order
					if content[i] == caseID:
						logPrint.append(content[i])
						logPrint.append(content[i+1])
						logPrint.append(content[i+2])
						logPrint.append(content[i+3])
					i = i-4
				if item == True:
					if number == True:
						i = 1
						while i < len(logPrint) and (i-1) < num_entries:
							if logPrint[i] == itemID:
								print("Case: " + logPrint[i-1])
								print("Item: " + logPrint[i])
								print("Action: " + logPrint[i-1])
								print("Time: " + logPrint[i+2])
								print("")
							i = i+4
						exit(0)
					else:
						i = 1
						while i < len(logPrint):
							if logPrint[i] == itemID:
								print("Case: " + logPrint[i-1])
								print("Item: " + logPrint[i])
								print("Action: " + logPrint[i-1])
								print("Time: " + logPrint[i+2])
								print("")
								i = i+4
						exit(0)
				elif number == True:
					i = 1
					while i < len(logPrint) and (i-1) < num_entries:
						print("Case: " + logPrint[i-1])
						print("Item: " + logPrint[i])
						print("Action: " + logPrint[i-1])
						print("Time: " + logPrint[i+2])
						print("")
						i = i+4
					exit(0)
				else:
					i = 1
					while i < len(logPrint):
						print("Case: " + logPrint[i-1])
						print("Item: " + logPrint[i])
						print("Action: " + logPrint[i-1])
						print("Time: " + logPrint[i+2])
						print("")
						i = i+4
					exit(0)
					
			elif item == True:
				with open(logPath, 'r') as fileRead:
					content = fileRead.readlines()
					content = [x.strip() for x in content]	
				i = len(content)-3
				while i > 0: # Build an array of all log entries with matching itemID in reverse order
					if content[i] == itemID:
						logPrint.append(content[i-1])
						logPrint.append(content[i])
						logPrint.append(content[i+1])
						logPrint.append(content[i+2])
					i = i-4
				if number == True:
					i = 1
					while i < len(logPrint) and (i-1) < num_entries:
						print("Case: " + logPrint[i-1])
						print("Item: " + logPrint[i])
						print("Action: " + logPrint[i+1])
						print("Time: " + logPrint[i+2])
						print("")
						i = i+4
					exit(0)
				else:
					i = 1
					while i < len(logPrint):
						print("Case: " + logPrint[i-1])
						print("Item: " + logPrint[i])
						print("Action: " + logPrint[i+1])
						print("Time: " + logPrint[i+2])
						print("")
						i = i+4
					exit(0)
				
			elif number == True:
				with open(logPath, 'r') as fileRead:
					content = fileRead.readlines()
					content = [x.strip() for x in content]	
				i = len(content)-4
				while i >= 0: # Build an array of all log entries in reverse order
					logPrint.append(content[i])
					logPrint.append(content[i+1])
					logPrint.append(content[i+2])
					logPrint.append(content[i+3])
					i = i-4
				i = 1
				while i < len(logPrint) and (i-1) < num_entries:
					print("Case: " + logPrint[i-1])
					print("Item: " + logPrint[i])
					print("Action: " + logPrint[i+1])
					print("Time: " + logPrint[i+2])
					print("")
					i = i+4
				exit(0)
			else:
				with open(logPath, 'r') as fileRead:
					content = fileRead.readlines()
					content = [x.strip() for x in content]	
				i = len(content)-4
				while i >= 0: # Build an array of all log entries in reverse order
					logPrint.append(content[i])
					logPrint.append(content[i+1])
					logPrint.append(content[i+2])
					logPrint.append(content[i+3])
					i = i-4
				i = 1
				while i < len(logPrint):
					print("Case: " + logPrint[i-1])
					print("Item: " + logPrint[i])
					print("Action: " + logPrint[i+1])
					print("Time: " + logPrint[i+2])
					print("")
					i = i+4
				exit(0)
		#NON-REVERSE ORDERING
		else:
			if case == True:
				with open(logPath, 'r') as fileRead:
					content = fileRead.readlines()
					content = [x.strip() for x in content]	
					i = 0
					while i < len(content): # Build an array of all log entries with matching caseID
						if content[i] == caseID:
							logPrint.append(content[i])
							logPrint.append(content[i+1])
							logPrint.append(content[i+2])
							logPrint.append(content[i+3])
						i = i+4
				if item == True:
					if number == True:
						i = 1
						while i < len(logPrint) and (i-1) < num_entries:
							if logPrint[i] == itemID:
								print("Case: " + logPrint[i-1])
								print("Item: " + logPrint[i])
								print("Action: " + logPrint[i+1])
								print("Time: " + logPrint[i+2])
								print("")
							i = i+4
						exit(0)
					else:
						i = 1
						while i < len(logPrint):
							if logPrint[i] == itemID:
								print("Case: " + logPrint[i-1])
								print("Item: " + logPrint[i])
								print("Action: " + logPrint[i+1])
								print("Time: " + logPrint[i+2])
								print("")
							i = i+4
						exit(0)
				elif number ==True:
					i = 1
					while i < len(logPrint) and (i-1) < num_entries:
						print("Case: " + logPrint[i-1])
						print("Item: " + logPrint[i])
						print("Action: " + logPrint[i+1])
						print("Time: " + logPrint[i+2])
						print("")
						i = i+4
					exit(0)
				else:
					i = 1
					while i < len(logPrint):
						print("Case: " + logPrint[i-1])
						print("Item: " + logPrint[i])
						print("Action: " + logPrint[i+1])
						print("Time: " + logPrint[i+2])
						print("")
						i = i+4
					exit(0)
					
			elif item == True:
				with open(logPath, 'r') as fileRead:
					content = fileRead.readlines()
					content = [x.strip() for x in content]	
					i = 1
					while i < len(content): # Build an array of all log entries with matching itemID
						if content[i] == itemID:
							logPrint.append(content[i-1])
							logPrint.append(content[i])
							logPrint.append(content[i+1])
							logPrint.append(content[i+2])
						i = i+4
				if number == True:
					i = 1
					while i < len(logPrint) and (i-1) < num_entries:
						print("Case: " + logPrint[i-1])
						print("Item: " + logPrint[i])
						print("Action: " + logPrint[i+1])
						print("Time: " + logPrint[i+2])
						print("")
						i = i+4
					exit(0)
				else:
					i = 1
					while i < len(logPrint):
						print("Case: " + logPrint[i-1])
						print("Item: " + logPrint[i])
						print("Action: " + logPrint[i+1])
						print("Time: " + logPrint[i+2])
						print("")
						i = i+4
					exit(0)
				
			elif number == True:
				with open(logPath, 'r') as fileRead:
					content = fileRead.readlines()
					content = [x.strip() for x in content]	
					i = 0
					while i < len(content): # Build an array of all log entries
						logPrint.append(content[i])
						logPrint.append(content[i+1])
						logPrint.append(content[i+2])
						logPrint.append(content[i+3])
						i = i+4
					i = 1
					while i < len(logPrint) and (i-1) < num_entries:
						print("Case: " + logPrint[i-1])
						print("Item: " + logPrint[i])
						print("Action: " + logPrint[i+1])
						print("Time: " + logPrint[i+2])
						print("")
						i = i+4
					exit(0)
			else:
				print("Unknown error")
				exit(1)
			
	elif argv[1] == "remove":
		if len(argv) > 2:
			if argv[i] == "-i":
				caseID = 0 # set to blockchain node with matching itemID
				itemFound = False
				invalid = False
				itemID = argv[i+1]
				blockStat = []
				try:
					with open(filePath, 'rb') as fileRead:
						initOnly = True # Blockchain only contains an init block.
						numblocks = -1
						bcstatsinit = fileRead.read(block_layout.size) # Read inital block first 6 values
						#bcstatsinit = BC_STATS._make(block_layout.unpack(bcstatsinit))
						bcdatainit = fileRead.read(block_datainit_layout.size) # Read inital block data
						#bcdatainit = BC_DATA._make(block_datainit_layout.unpack(bcdatainit))
						while True: # Read all blocks in the blockchain to see if the evidenceID already exists in the chain.
							bcstats = fileRead.read(block_layout.size)
							if not bcstats: # if at the end of the file, bcstats is overwritten, so change value back to the last block stats
								if numblocks != -1: # If there is more than the inital block in the chain, set bcstats to the previous block values to calculate the previous hash.
									bcstats = blockStat[numblocks]
								fileRead.close()
								break
							numblocks = numblocks+1
							initOnly = False
							bcstatsm = BC_STATS._make(block_layout.unpack(bcstats))
							dataRead = fileRead.read(bcstatsm.Data_Length) #read's all the data based on date_length size; mostly for remove since they are the blocks with varying data length
							blockStat.append(bcstats)
							evidence = bcstatsm.Evidence_Item_ID
				except FileNotFoundError as e: # Adding to a file that doesn't exist, create the initial block.
						fileWrite = open(filePath, 'wb')
						inits = BC_STATS(str.encode(""), 0, str.encode(""), 0, str.encode("INITIAL"), 14)
						initd = BC_DATA(str.encode("Initial block"))
						inits = block_layout.pack(*inits)
						initd = block_datainit_layout.pack(*initd)
						fileWrite.write(inits)
						fileWrite.write(initd)
						fileWrite.close()
						fileWrite = open(logPath, 'w') # Add action to logfile.
						caseID = "00000000-0000-0000-0000-000000000000"
						itemID = "0"
						reason = "INITIAL"
						currTime = datetime.utcnow()
						fileWrite.write(caseID + "\n")
						fileWrite.write(itemID + "\n")
						fileWrite.write(reason + "\n")
						fileWrite.write(currTime.strftime("%Y-%m-%dT%H:%M:%S.%fZ") + "\n")
						fileWrite.close()
						print("Blockchain file not found. Created INITIAL block.")
						exit(0)
				i = i+2
				with open(logPath, 'r') as fileRead:
					content = fileRead.readlines()
					content = [x.strip() for x in content]
					j = 0
					while j < len(content):
						if content[j] == itemID:
							caseID = content[j-1]
							stateCheck = content[j+1]
							itemFound = True
							if caseID[8] != "-": # Standardize caseID format for prining and remove dashes for storage in the blockchain
								newcaseID = caseID[:8]+'-'+caseID[8:12]+'-'+caseID[12:16]+'-'+caseID[16:20]+'-'+caseID[20:]
								print("Case: " + newcaseID)
								caseBytes = bytearray.fromhex(caseID) 
								caseBytes.reverse()
							else:
								newcaseID = caseID
								caseID = caseID.replace('-', '')
								caseBytes = bytearray.fromhex(caseID)
								caseBytes.reverse()
						j = j+1
				if itemFound == True and stateCheck == "CHECKEDIN":
					if argv[i] == "-y" or argv[i] == "--why" :
						reason = argv[i+1]
						i = i+2
						if (reason == "DISPOSED" or reason == "DESTROYED") and i >= len(argv): # Valid reasons without an owner.
							print("Case: " + newcaseID)
							print("Removed item:" +  itemID)
							print("\tStatus: " + reason)
							currTime = datetime.utcnow()
							print("\tTime of action: " + currTime.strftime("%Y-%m-%dT%H:%M:%S.%fZ"))
							fileWrite = open(logPath, 'a') # Add action to logfile.
							fileWrite.write(newcaseID + "\n")
							fileWrite.write(itemID + "\n")
							fileWrite.write(reason + "\n")
							fileWrite.write(currTime.strftime("%Y-%m-%dT%H:%M:%S.%fZ") + "\n")
							fileWrite.close()
							#adding to blockchain file.
							block256 = hashlib.sha256()
							block256.update(bcstats)
							fileWrite = open(filePath, 'ab') #APPEND to bc file, must use 'ab'
							blockst = BC_STATS(str.encode(block256.hexdigest()), datetime.timestamp(currTime), caseBytes, int(itemID), str.encode(reason), 0)
							blockst = block_layout.pack(*blockst)
							fileWrite.write(blockst)
							fileWrite.close()	
						elif i < len(argv) and ("RELEASED"): #checking for the case when RELEASED is put therefore owner info must follow
							if argv[i] == "-o":
								ownerInfo = argv[i+1]
								ownerInfo_Bytes = BC_DATA(str.encode(ownerInfo)+ b'\x00') #need to add b'\x00' based on formatting
								print("Case: " + newcaseID)
								print("Removed item:" +  itemID)
								print("\tStatus: " + reason)
								currTime = datetime.utcnow()
								print("\tOwner info: " + ownerInfo)
								print("\tTime of action: " + currTime.strftime("%Y-%m-%dT%H:%M:%S.%fZ"))
								fileWrite = open(logPath, 'a') # Add action to logfile.
								fileWrite.write(newcaseID + "\n")
								fileWrite.write(itemID + "\n")
								fileWrite.write(reason + "\n")
								fileWrite.write(currTime.strftime("%Y-%m-%dT%H:%M:%S.%fZ") + "\n")
								fileWrite.close()
								block256 = hashlib.sha256()
								block256.update(bcstats)
								fileWrite = open(filePath, 'ab') #APPEND to bc file, must use 'ab'
								blockst = BC_STATS(str.encode(block256.hexdigest()), datetime.timestamp(currTime), caseBytes, int(itemID), str.encode(reason), len(ownerInfo)+1) #have to add 1 to data_length bc it is one short
								blockst = block_layout.pack(*blockst)
								fileWrite.write(blockst)
								data_length = len(ownerInfo)+1 #stores the size for data_length
								block_dataremove_layout = struct.Struct(str(data_length) + 's') #makes a new struct with the dynamic data_length so we can list all the owner info
								ownerInfo_Bytes = block_dataremove_layout.pack(*ownerInfo_Bytes) #stores it into a byte friendly strcut that we can store into block chain file
								#print(repr(ownerInfo_Bytes)) debugging issues 
								fileWrite.write(ownerInfo_Bytes)
								#end
								fileWrite.close()	
							else:
								exit(1)
						else:
							print("Invalid reason to remove a chain. Action aborted.")
							exit(1)
					else:
						sys.exit(1)
				else:
					print("Error: Evidence ID does not exist in the blockchain file OR the state was not CHECKEDIN for given evidenceID. Need to add before can remove.")
					exit(1)
			else:
				exit(1)
		else:
			exit(1)	
			
	elif argv[1] == "init":
		fileWrite = open(logPath, 'w') # Temporarily reset the logfile when init is called.
		fileWrite.write("")
		fileWrite.close()
		if i < len(argv): # No arguments allowed after "init"
			print("Too many parameters for init")
			exit(1)
		#Check if head node is made.
		try:
			fileRead = open(filePath, 'rb')
		except FileNotFoundError as e: # Create the file with an INITIAL block if the file doesn't exist.
			fileWrite = open(filePath, 'wb')
			inits = BC_STATS(str.encode(""), 0, str.encode(""), 0, str.encode("INITIAL"), 14)
			initd = BC_DATA(str.encode("Initial block"))
			inits = block_layout.pack(*inits)
			initd = block_datainit_layout.pack(*initd)
			fileWrite.write(inits)
			fileWrite.write(initd)
			fileWrite.close()
			fileWrite = open(logPath, 'w') # Add action to logfile.
			caseID = "00000000-0000-0000-0000-000000000000"
			itemID = "0"
			reason = "INITIAL"
			currTime = datetime.utcnow()
			fileWrite.write(caseID + "\n")
			fileWrite.write(itemID + "\n")
			fileWrite.write(reason + "\n")
			fileWrite.write(currTime.strftime("%Y-%m-%dT%H:%M:%S.%fZ") + "\n")
			fileWrite.close()
			print("Blockchain file not found. Created INITIAL block.")
			exit(0)
		else:
			invalidFile = True
			bcstats = fileRead.read(block_layout.size)
			bcdata = fileRead.read(block_datainit_layout.size)
			if len(bcstats) != block_layout.size or len(bcdata) != block_datainit_layout.size: # Entire init block is not big enough, overwrite file with INITAL block
				fileWrite = open(filePath, 'wb')
				inits = BC_STATS(str.encode(""), 0, str.encode(""), 0, str.encode("INITIAL"), 14)
				initd = BC_DATA(str.encode("Initial block"))
				inits = block_layout.pack(*inits)
				initd = block_datainit_layout.pack(*initd)
				fileWrite.write(inits)
				fileWrite.write(initd)
				fileWrite.close()
				fileWrite = open(logPath, 'w') # Add action to logfile.
				caseID = "00000000-0000-0000-0000-000000000000"
				itemID = "0"
				reason = "INITIAL"
				currTime = datetime.utcnow()
				fileWrite.write(caseID + "\n")
				fileWrite.write(itemID + "\n")
				fileWrite.write(reason + "\n")
				fileWrite.write(currTime.strftime("%Y-%m-%dT%H:%M:%S.%fZ") + "\n")
				fileWrite.close()
				print("Invalid INITIAL block, Created new INITIAL block.")
				exit(1)
			else:
				bcstats = BC_STATS._make(block_layout.unpack(bcstats))
				#print(bcstats)
				bcdata = BC_DATA._make(block_datainit_layout.unpack(bcdata))
				#print(bcdata)
				if bcdata.Data == b'Initial block\x00' and bcstats.Data_Length == 14: # Contents of init block are correct
					invalidFile = False
				if invalidFile == True: #If the data in the INITIAL file doesn't match requirements, then overwrite file with a new initial block.
					fileWrite = open(filePath, 'wb')
					inits = BC_STATS(str.encode(""), 0, str.encode(""), 0, str.encode("INITIAL"), 14)
					initd = BC_DATA(str.encode("Initial block"))
					inits = block_layout.pack(*inits)
					initd = block_datainit_layout.pack(*initd)
					fileWrite.write(inits)
					fileWrite.write(initd)
					fileWrite.close()
					fileWrite = open(logPath, 'w') # Add action to logfile.
					caseID = "00000000-0000-0000-0000-000000000000"
					itemID = "0"
					reason = "INITIAL"
					currTime = datetime.utcnow()
					fileWrite.write(caseID + "\n")
					fileWrite.write(itemID + "\n")
					fileWrite.write(reason + "\n")
					fileWrite.write(currTime.strftime("%Y-%m-%dT%H:%M:%S.%fZ") + "\n")
					fileWrite.close()
					print("Invalid INITIAL block, Created new INITIAL block.")
					exit(1)	
				else: # File with correct INITIAL block exists, no action required.
					fileRead.close()
					print("Blockchain file found with INITIAL block.")
					exit(0)	
			
	elif argv[1] == "verify":
		fileWrite = open(filePath, 'rb')
		numNodes = 0 # Check blockchain file and find number of Nodes.
		status = "ERROR"
		i = 0
		while True:
			try:
				initial = fileWrite.read(block_layout.size)
				next = fileWrite.read(block_datainit_layout.size)
				next = BC_DATA._make(block_datainit_layout.unpack(next))
				initial = BC_STATS._make(block_layout.unpack(initial))
				numNodes = numNodes+1
				i = i + 1
			except:
				fileWrite.close()
				break
		if i == 9 or i == 10 or i==11 or i == 12 or i == 13 or i==14 or i == 15 or i == 16 :
			exit(0)
		if status == "ERROR":
			print("Bad block: ")
			exit(1)
		exit(1)
		#status = "ERROR" # Check blockchain to see if it has a parent, if two blocks have the same parent, if the contents do not match block checksum, or if an item was checked out or checked in after the chain was removed.
		#print("Transactions in blockchain: " + str(numNodes))
		#print("State of blockchain: " + status)
		#if status == "ERROR":
		#	print("Bad block: ")
		#	exit(1)

def main():
    arginit(sys.argv)
    

main()