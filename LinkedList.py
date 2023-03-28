#!/usr/bin/env python3
from Node import Node
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
        current = self.head
        if current:
            while current.next:
                current = current.next
            current.next = newNode
        else:
            self.head = newNode

    def size(self):
        current = self.head
        count = 0
        while current:
            count += 1
            current = current.next
        return count
    def print(self):
        current = self.head
        while current != None:
            print("Previous hash: " + str(current.previousHash) + ", Timestamp: " + str(current.timestamp) +", CaseID: " + str(current.caseID) + ", EvidenceID: " + str(current.evidenceID) + ", State: " + str(current.state) +", Data Length: " + str(current.dataLength) +", Data: " + str(current.data))
            current = current.next
        return True
    
    def find(self, target):
        current = self.head
        while current:
            if current == target:
                return current
        else:
            current = current.next
            
    def checkstate(self, id):
        current = self.head
        while current:
            if current.evidenceID == id:
                return current.state
        else:
            current = current.next
        return "N/A"
                
    def remove(self, id):
        #Deletes a node given a specified id
        current = self.head
        while current:
            if current.evidenceID == id:
                if current.state == "CHECKEDIN":
                    current.state = "RELEASED"
                    print("Case:" + str(current.caseID))
                    print("Removed item: " + str(current.evidenceID))
                    print("\tStatus: " + str(current.state))
                    print("\tOwner info: NEED TO IMPLEMENT TO TAKE OWNER INFO FROM ARGS & PLACE HERE")
                    print("\tTime of action:" + str(current.timestamp))
                    return True
                else:
                    #Error Code will need to be generated for this; for example if they do 'echo $?' then it would need to return our predefined integer value for this error
                    current.state = "ERROR"
                    print("Error: Cannot remove an evidence item that is not CHECKEDIN.")
                    return False
            else:
                current = current.next
        print("ERROR: NOT FOUND")
        return False

    def add(self, newElement, position):
        #insert a new node at given position
        count = 1
        current = self.head
        if position == 1:
            newElement.next = self.head
            self.head = newElement
        while current:
            if count + 1 == position:
                newElement.next = current.next
                current.next = newElement
                return
            else:
                count += 1
                current = current.next
        pass

    def checkout(self, id):
        #Returns true if found & returns false if not found
        #takes the LL as a param and the item_id
        # changes to CHECKEDOUT state for an evidence item given its item_id
        #should display its case(hash), item_id, new status of evidence, time
        current = self.head
        test = Node
        while current:
            if current.evidenceID == id:
                if current.state == "CHECKEDIN":
                    current.state = 'CHECKEDOUT'
                    print("Case: " + str(current.caseID))
                    print("Checked out Item: " + str(current.evidenceID))
                    print("\t Status: " + str(current.state))
                    print("\t Time of action: " + str(current.timestamp))
                    return True
                else:
                    #Error Code will need to be generated for this; for example if they do 'echo $?' then it would need to return our predefined integer value for this error
                    current.state = "ERROR"
                    print("Error: Cannot check out a checked out item. Must check it in first.")
                    return False
            else:
                current = current.next
        print("ERROR: NOT FOUND")
        return False

    def checkin(self, id):
        #Returns true if found & returns false if not found
        #takes the LL as a param and the item_id
        #changes to CHECKEDIN state for an evidence item given its item_id
        #should display its case(hash), item_id, new status of evidence, time
        current = self.head
        while current:
            if current.evidenceID == id:
                if current.previousHash != None:
                    current.state = 'CHECKEDIN'
                    print("Case: " + str(current.caseID))
                    print("Checked out Item: " + str(current.evidenceID))
                    print("\t Status: " + str(current.state))
                    print("\t Time of action: " + str(current.timestamp))
                    return True
                else:
                    #Error Code will need to be generated for this; for example if they do 'echo $?' then it would need to return our predefined integer value for this error
                    current.state = "ERROR"
                    print("Error: Checkin actions may only be performed on evidence items that have already been added to the blockchain. No previous hash found so not added.")
                    return False
            else:
                current = current.next
        print("ERROR: NOT FOUND")
        return False
    
    def verify(self):
        #Traverses the blockchain & checks for any error states.
        #Will return # of blocks & the state of the blockchain.
        #If the state is ERROR then that means at least one block had an error & will need to return: bad blocks hash, & reason for error.
        #Parent block not found, same parent block for more than one block, block contents do not match block checksum, trying to checkin/checkout after removing block
        num = self.size()
        current = self.head
        print("Transactions in blockchain: " + str(num))
        while current:
            #Do we print all errors or just first one found?
            if current.state == "ERROR":
                print("State of blockchain: " + current.state)
                #needs to be a hash with no hyphens in it
                print("Bad block: " + current.previousHash)
                #needs to see the reason for error - possibly add that in to node struct
                print("NEED TO IMPLEMENT REASON - if parent block issue need to list it's hash(If it has one!) otherwise just print the error")
                return False
            else:
                current = current.next
        print("State of blockchain: CLEAN") 
        return True