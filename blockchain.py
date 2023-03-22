#!/bin/env python3
import Node
import LinkedList


class Node(object):
    def __init__(self, previousHash, timestamp, caseID, evidenceID, state, dataLength, data):
        self.previousHash = previousHash
        self.timestamp = timestamp
        self.caseID = caseID
        self.evidenceID = evidenceID
        self.state = state
        self.dataLength = dataLength
        self.data = data
        self.next = None


def main():
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

main()