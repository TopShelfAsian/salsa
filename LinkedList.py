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

    def insert(self, newElement, position):
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

    def print(self):
        current = self.head
        while current:
            print(current.evidenceID)
            current = current.next