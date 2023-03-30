#!/usr/bin/env python3
from Node import Node
from datetime import datetime
class LinkedList(object):
    def __init__(self, head=None):
        self.head = head

    def init(self):
        if self.head == None:
            print("Blockchain file not found. Created INITIAL block.")
            head = Node(None, 69, None, None, "INITIAL", 0x0E, "Initial block")
            self.head = head
            return False
        else:
            print("Blockchain file found with INITIAL block.")
            return True


    def append(self, newNode):
        temp = self.head
        if temp:
            while temp.next:
                temp = temp.next
            temp.next = newNode
        else:
            self.head = newNode

    def size(self):
        temp = self.head
        count = 0
        while temp:
            count += 1
            temp = temp.next
        return count
    
    def print(self):
        temp = self.head
        while temp != None:
            print("Previous hash: " + str(temp.previousHash) + ", Timestamp: " + str(temp.timestamp) +", CaseID: " + str(temp.caseID) + ", EvidenceID: " + str(temp.evidenceID) + ", State: " + str(temp.state) +", Data Length: " + str(temp.dataLength) +", Data: " + str(temp.data))
            temp = temp.next
        return True
    
    def find(self, target):
        temp = self.head
        while temp:
            if temp == target:
                return temp
        else:
            temp = temp.next

    #used to check the state of a block        
    def checkstate(self, id):
        temp = self.head
        while temp:
            if temp.evidenceID == id:
                return temp.state
        else:
            temp = temp.next
        return "N/A"
    
    #Used for add & checking if the evidenceID is already in use
    def checkEID(self, id):
        temp = self.head
        while temp:
            if temp.evidenceID == id:
                return True
            else:
                temp = temp.next
        return False
    
    def printLog(self):
        temp = self.head.next
        while temp:
            print("Case: " + temp.caseID)
            print("Item: " + temp.evidenceID)
            print("Action: " + temp.state)
            print("Time: " + temp.timestamp + "\n")
            temp = temp.next
        return 
    
    #https://www.geeksforgeeks.org/python-program-for-reverse-a-linked-list/
    def reverseLL(self):
        previous = None
        temp = self.head
        while(temp != None):
            next = temp.next
            temp.next = previous
            previous = temp
            temp = next
        self.head = previous
    
    def log(self, eID, count):
        log_ll = LinkedList()
        #made it the node after head bc I don't think we need to print head in log 
        #This covers the most basic test case that they call log with no flags
        if count == 0 & eID == None:
            log_ll = self
            #reverses the LL so it prints the ALL the LL
            log_ll.reverseLL()
            log_ll.printLog()
            return


        return True

    def add(self, cID, eID):
        #insert a new block into the blockchain given the caseID & the evidenceID
        temp = self.head
        flag = self.checkEID(eID)
        if flag == True:
            #Error Code will need to be generated for this; for example if they do 'echo $?' then it would need to return our predefined integer value for this error
            print("Error: Evidence ID already exits")
            return
        else:
            newBlock = Node(None, None, cID, eID, "CHECKEDIN", None, None)
            self.append(newBlock)
            #NEED TO BE FIXED: if multiple evidence ID's we only print case id once & added item(eid), status, & time of action need to printed for each eID
            print("Case:" + str(newBlock.caseID))
            print("Added item: " + str(newBlock.evidenceID))
            print("\tStatus: " + str(newBlock.state))
            timeOfAction = datetime.now()
            iso_timeOfAction = datetime.isoformat(timeOfAction)
            print("\tTime of action: " + str(timeOfAction))
            return
                
    def remove(self, id):
        #Deletes a node given a specified id
        temp = self.head
        while temp:
            if temp.evidenceID == id:
                if temp.state == "CHECKEDIN":
                    temp.state = "RELEASED"
                    print("Case:" + str(temp.caseID))
                    print("Removed item: " + str(temp.evidenceID))
                    print("\tStatus: " + str(temp.state))
                    #timeOfAction = datetime.now()
                    #iso_timeOfAction = datetime.isoformat(timeOfAction)
                    #print("\tTime of action: " + str(timeOfAction))
                    return True
                else:
                    #Error Code will need to be generated for this; for example if they do 'echo $?' then it would need to return our predefined integer value for this error
                    temp.state = "ERROR"
                    print("Error: Cannot remove an evidence item that is not CHECKEDIN.")
                    return False
            else:
                temp = temp.next
        print("ERROR: NOT FOUND")
        return False

    def checkout(self, id):
        #Returns true if found & returns false if not found
        #takes the LL as a param and the item_id
        # changes to CHECKEDOUT state for an evidence item given its item_id
        #should display its case(hash), item_id, new status of evidence, time
        temp = self.head
        test = Node
        while temp:
            if temp.evidenceID == id:
                if temp.state == "CHECKEDIN":
                    temp.state = 'CHECKEDOUT'
                    print("Case: " + str(temp.caseID))
                    print("Checked out Item: " + str(temp.evidenceID))
                    print("\t Status: " + str(temp.state))
                    timeOfAction = datetime.now()
                    iso_timeOfAction = datetime.isoformat(timeOfAction)
                    print("\tTime of action: " + str(timeOfAction))
                    return True
                else:
                    #Error Code will need to be generated for this; for example if they do 'echo $?' then it would need to return our predefined integer value for this error
                    temp.state = "ERROR"
                    print("Error: Cannot check out a checked out item. Must check it in first.")
                    return False
            else:
                temp = temp.next
        print("ERROR: NOT FOUND")
        return False

    def checkin(self, id):
        #Returns true if found & returns false if not found
        #takes the LL as a param and the item_id
        #changes to CHECKEDIN state for an evidence item given its item_id
        #should display its case(hash), item_id, new status of evidence, time
        temp = self.head
        while temp:
            if temp.evidenceID == id:
                if temp.previousHash != None:
                    temp.state = 'CHECKEDIN'
                    print("Case: " + str(temp.caseID))
                    print("Checked out Item: " + str(temp.evidenceID))
                    print("\t Status: " + str(temp.state))
                    timeOfAction = datetime.now()
                    iso_timeOfAction = datetime.isoformat(timeOfAction)
                    print("\tTime of action: " + str(timeOfAction))
                    return True
                else:
                    #Error Code will need to be generated for this; for example if they do 'echo $?' then it would need to return our predefined integer value for this error
                    temp.state = "ERROR"
                    print("Error: Checkin actions may only be performed on evidence items that have already been added to the blockchain. No previous hash found so not added.")
                    return False
            else:
                temp = temp.next
        print("ERROR: NOT FOUND")
        return False
    
    def verify(self):
        #Traverses the blockchain & checks for any error states.
        #Will return # of blocks & the state of the blockchain.
        #If the state is ERROR then that means at least one block had an error & will need to return: bad blocks hash, & reason for error.
        #Parent block not found, same parent block for more than one block, block contents do not match block checksum, trying to checkin/checkout after removing block
        num = self.size()
        temp = self.head
        print("Transactions in blockchain: " + str(num))
        while temp:
            #Do we print all errors or just first one found?
            if temp.state == "ERROR":
                print("State of blockchain: " + temp.state)
                #needs to be a hash with no hyphens in it
                print("Bad block: " + temp.previousHash)
                #needs to see the reason for error - possibly add that in to node struct
                print("NEED TO IMPLEMENT REASON - if parent block issue need to list it's hash(If it has one!) otherwise just print the error")
                return False
            else:
                temp = temp.next
        print("State of blockchain: CLEAN") 
        return True