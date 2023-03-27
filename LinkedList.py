#!/usr/bin/env python3
from Node import Node
class LinkedList(object):
    def __init__(self, head=None):
        self.head = head

    def append(self, newNode):
        current = self.head
        if current:
            while current.next:
                current = current.next
            current.next = newNode
        else:
            self.head = newNode

    def print(self):
        current = self.head
        while current:
            print(current.evidenceID)
            current = current.next
    
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
                
    def delete(self, value):
        #Delete first note with a given value
        current = self.head
        if current.evidenceID == value:
            self.head = current.next
        else:
            while current:
                if current.evidenceID == value:
                    break
                prev = current
                current = current.next
            if current == None:
                return
            prev.next = current.next
            current = None

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
        # changes to checkout entry for an evidence item given its item_id
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
                    print("Error: Cannot check out a checked out item. Must check it in first.")
                    return False
            else:
                current = current.next
        print("ERROR: NOT FOUND")
        return False
        