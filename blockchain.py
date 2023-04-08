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
	i = 2
	itemIDs = []
	if (len(argv) == 1): # No arugments to the program, abort
		exit(3)
	if argv[1] == "add":
		blockStat = [] # Array storing the blocks read from the blockchain
		if len(argv) > 2:
			if argv[i] == "-c": # Case ID
				caseID = argv[i+1]
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
				checkedOut = False;
				#Fetch caseID of block with matching itemID and block info
				print("Case: ")
				
				if checkedOut == False:
					print("Checked out item: " + argv[i+1])
					print(" Status: ")
					print(" Time of action: ")
				else:
					print("Error: Cannot check out a checked out item. Must check in first.")
					exit(1)
			else:
				exit(1)
		else:
			exit(1)
		
	elif argv[1] == "checkin":
		if len(argv) > 2:
			if argv[i] == "-i":
				#Fetch caseID of block with matching itemID and block info
				print("Case: ")
				print("Checked in item: " + argv[i+1])
				print(" Status: ")
				print(" Time of action: ")
			else:
				exit(1)
		else:
			exit(1)
			
	elif argv[1] == "log":
		if len(argv) > 2:
			if argv[i] == "-r" or argv[i] == "--reverse": # Reverse order of log entries printed
				#Fetch caseID of block with matching itemID and block info
				print("Case: ")
				print("Checked in item: ")
				print(" Status: ")
				print(" Time of action: ")
			#elif argv[i] == "-n": Set number of log entries
			
			#elif argv[i] == "-i": # Find log entries with matched itemID
			
			#elif argv[i] == "-c": # Find log entries with matched caseID
			
			#else: # Print all contents of the log.
		else:
			exit(1)
			
	elif argv[1] == "remove":
		if len(argv) > 2:
			if argv[i] == "-i":
				caseID = 0 # set to blockchain node with matching itemID
				i = i+2
				if argv[i] == "-y" or argv[i] == "--why" :
					print("Case: ")
					print("Removed item:" + argv[i-1])
					print(" Status: ")
					i = i+2
					if i < len(argv):
						if argv[i] == "-o":
							print(" Owner info: " + argv[i+1])
							print(" Time of action: ")
						else:
							exit(1)
				else:
					sys.exit(1)
					
			else:
				exit(1)
		else:
			exit(1)	
			
	elif argv[1] == "init":
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
					print("Invalid INITIAL block, Created new INITIAL block.")
					exit(1)	
				else: # File with correct INITIAL block exists, no action required.
					fileRead.close()
					print("Blockchain file found with INITIAL block.")
					exit(0)	
			
	elif argv[1] == "verify":
		numNodes = 0 # Check blockchain file and find number of Nodes.
		status = "CLEAN" # Check blockchain to see if it has a parent, if two blocks have the same parent, if the contents do not match block checksum, or if an item was checked out or checked in after the chain was removed.
		print("Transactions in blockchain: " + str(numNodes))
		print("State of blockchain: " + status)
		if status == "ERROR":
			print("Bad block: ")

def main():
    arginit(sys.argv)
    

main()
