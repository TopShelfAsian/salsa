#!/bin/env python3
from datetime import datetime

test = datetime.now()
test2 = datetime.isoformat(test)
class Node(object):
    def __init__(self, previousHash, timestamp, caseID, evidenceID, state, dataLength, data):
        self.previousHash = previousHash
        self.timestamp = test2
        self.caseID = caseID
        self.evidenceID = evidenceID
        self.state = state
        self.dataLength = dataLength
        self.data = data
        self.next = None