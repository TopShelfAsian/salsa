#!/usr/bin/env python3
import sys
import getopt
import hashlib
import collections
import struct
import os
from datetime import datetime
import time

block_layout = struct.Struct(b'32s d 16s I 12s I')
block_datainit_layout = struct.Struct(b'14s ')
block_data_layout = struct.Struct('0s ') 
BC_STATS = collections.namedtuple('BC_STATS', ['Previous_Hash', 'Timestamp', 'Case_ID', 'Evidence_Item_ID', 'State', 'Data_Length'])
BC_DATA = collections.namedtuple('BC_DATA', ['Data'])
bc_list = collections.namedtuple('bc_list', ['Case','ID', 'Status', 'Time'])
bc_checkout = collections.namedtuple('bc_checkout', ['ID', 'Status'])

	
def arginit(argv):
	key = 'BCHOC_FILE_PATH'
	if key in os.environ:
		filePath = os.environ[key]
	else:
		filePath = "bchocout"
	i = 2
	itemIDs = []
	if (len(argv) == 1):
		exit(3)
	if argv[1] == "add":
		blockStat = []
		if len(argv) > 2:
			if argv[i] == "-c":
				caseID = argv[i+1]
				i = i+2
				numitems = -1
				if i >= len(argv):
					print("No evidence ID given, aborted.")
					exit(1) # no evidence id given, not possible
				while i < len(argv):
					if argv[i] == "-i":
						itemFound = False
						itemIDs.append(argv[i+1])
						numitems = numitems+1
						#Check if evidence id exists in chain, if it does, do not add
	
						try:
							with open(filePath, 'rb') as fileRead:
								initOnly = True
								numblocks = -1
								bcstatsinit = fileRead.read(block_layout.size)
								#bcstatsinit = BC_STATS._make(block_layout.unpack(bcstatsinit))
								bcdatainit = fileRead.read(block_datainit_layout.size)
								#bcdatainit = BC_DATA._make(block_datainit_layout.unpack(bcdatainit))
								while True:
									bcstats = fileRead.read(block_layout.size)
									if not bcstats: # if at the end of the file, bcstats is overwritten, so change value back to the last block stats
										if numblocks != -1:
											bcstats = blockStat[numblocks]
										fileRead.close()
										break
									numblocks = numblocks+1
									initOnly = False
									bcstatsm = BC_STATS._make(block_layout.unpack(bcstats))
									blockStat.append(bcstats)
									evidence = bcstatsm.Evidence_Item_ID
									if str(evidence) == itemIDs[numitems]:
										itemFound = True
						except FileNotFoundError as e:
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
								
						
						#If the evidence item doesn't exist, peform the hash of the last item and append to the file
						if itemFound == False:
							if caseID[8] != "-":
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
							#TO DO: Add caseID, itemID to blockchain Node, establish Node
							print("\tStatus: CHECKEDIN")
							currTime = datetime.utcnow()
							print("\tTime of action: " + currTime.strftime("%Y-%m-%dT%H:%M:%S.%fZ"))
							if initOnly == True:
								fileWrite = open(filePath, 'ab') #APPEND to bc file, must use 'ab'
								secondst = BC_STATS(str.encode(""), datetime.timestamp(currTime), caseBytes, int(itemIDs[numitems]), str.encode("CHECKEDIN"), 0)
								secondst = block_layout.pack(*secondst)
								print(secondst)
								fileWrite.write(secondst)
								fileWrite.close()
							else:
								block256 = hashlib.sha256()
								
								block256.update(bcstats)
								fileWrite = open(filePath, 'ab') #APPEND to bc file, must use 'ab'

								blockst = BC_STATS(str.encode(block256.hexdigest()), datetime.timestamp(currTime), caseBytes, int(itemIDs[numitems]), str.encode("CHECKEDIN"), 0)
								blockst = block_layout.pack(*blockst)
								print(blockst)
								fileWrite.write(blockst)
								fileWrite.close()
						else:
							print("Trying to add duplicate block, aborted.")
							exit(1)
							
					else:
						exit(1)
					i = i+2
					
			else:
				exit(1)
		else:
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
		if i < len(argv): # no arguments allowed after "init"
			print("Too many parameters for init")
			exit(1)
		#Check if head node is made.
		try:
			fileRead = open(filePath, 'rb')
		except FileNotFoundError as e:
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
			if len(bcstats) != block_layout.size or len(bcdata) != block_datainit_layout.size: # entire init block is not big enough
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
				if bcdata.Data == b'Initial block\x00' and bcstats.Data_Length == 14: # contents of init block are correct
					invalidFile = False
				if invalidFile == True:
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
