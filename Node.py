#!/bin/env python3

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