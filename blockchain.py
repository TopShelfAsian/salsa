#!/usr/bin/env python3
import sys
import getopt
import hashlib
import collections
import struct
import os
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
		if len(argv) > 2:
			if argv[i] == "-c":
				caseID = argv[i+1]
				print("Case: " + caseID)
				i = i+2
				numitems = 0
				while i < len(argv):
					if argv[i] == "-i":
						itemIDs.append(argv[i+1])
						print("Added item: " + itemIDs[numitems])
						numitems = numitems+1
						#TO DO: Add caseID, itemID to blockchain Node, establish Node
						print(" Status: ")
						print(" Time of action: ")
					else:
						exit(3)
					i = i+2
					
			else:
				exit(3)
		else:
			exit(3)	
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
				exit(3)
		else:
			exit(3)
		
	elif argv[1] == "checkin":
		if len(argv) > 2:
			if argv[i] == "-i":
				#Fetch caseID of block with matching itemID and block info
				print("Case: ")
				print("Checked in item: " + argv[i+1])
				print(" Status: ")
				print(" Time of action: ")
			else:
				exit(3)
		else:
			exit(3)
	elif argv[1] == "log":
		if len(argv) > 2:
			if argv[i] == "-r": # Reverse order of log entries printed
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
			exit(3)
	elif argv[1] == "remove":
		if len(argv) > 2:
			if argv[i] == "-i":
				caseID = 0 # set to blockchain node with matching itemID
				i = i+2
				if argv[i] == "-y":
					print("Case: ")
					print("Removed item:" + argv[i-1])
					print(" Status: ")
					i = i+2
					if argv[i] == "-o":
						print(" Owner info: " + argv[i+1])
					print(" Time of action: ")
				else:
					sys.exit(3)
					
			else:
				exit(3)
		else:
			exit(3)	
	elif argv[1] == "init":
		#Check if head node is made.
		try:
			fileRead = open(filePath, 'rb')
			bcstats = fileRead.read(block_layout.size)
			bcdata = fileRead.read(block_datainit_layout.size)
			bcstats = BC_STATS._make(block_layout.unpack(bcstats))
			print(bcstats)
			bcdata = BC_DATA._make(block_datainit_layout.unpack(bcdata))
			print(bcdata)
			fileRead.close()
			print("Blockchain file found with INITIAL block.")
			exit(0)
		except FileNotFoundError as e:
			fileWrite = open(filePath, 'wb')
			inits = BC_STATS(str.encode("None"), time.time(), str.encode("None"), 0, str.encode("INITIAL"), 14)
			initd = BC_DATA(str.encode("Initial block"))
			inits = block_layout.pack(*inits)
			initd = block_datainit_layout.pack(*initd)
			fileWrite.write(inits)
			fileWrite.write(initd)
			fileWrite.close()
			print("Blockchain file not found. Created INITIAL block.")
			exit(0)

			
	elif argv[1] == "verify":
		numNodes = 0 # Check blockchain file and find number of Nodes.
		status = "CLEAN" # Check blockchain to see if it has a parent, if two blocks have the same parent, if the contents do not match block checksum, or if an item was checked out or checked in after the chain was removed.
		print("Transactions in blockchain: " + str(numNodes))
		print("State of blockchain: " + status)
		if status == "ERROR":
			print("Bad block: ")
	
	print("Testing for group!")
	var = input("PLease input a number: ")
	e1 = Node(1,1,1,1,1,1,1)
	e2 = Node(2,2,2,2,2,2,2)
	e3 = Node(3,3,3,3,3,3,3)
	e4 = Node(4,4,4,4,4,4,4)

	ll = LinkedList(e1)
	ll.append(e2)
	ll.append(e3)

	print("Print 3", ll.head.next.next.evidenceID)

	ll.insert(e4,3)
	ll.delete(1)
	print(ll.print())

def main():
    arginit(sys.argv)
    

main()
