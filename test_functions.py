#!/usr/bin/env python3
from Node import Node
from LinkedList import LinkedList
from datetime import datetime
import sys
import getopt

#Passing functions:
#   checkout, checkin, remove, verify(still needs a little more detail), init
#Faiing functions:
# add, log
def main():
	print("Testing funtions")
	print("Note: case ID's last char is the difference")
	e1 = Node("AAAAA-BBBBB-CCCCC-DDDDD",1200,"65cc391d-6568-4dcc-a3f1-86a2f04140f3",11111,"CHECKEDOUT",69,22)
	e2 = Node("EEEEE-FFFFF-GGGGG-HHHHH",1201,"65cc391d-6568-4dcc-a3f1-86a2f04140f4",22222,"CHECKEDIN",69,22)
	e3 = Node("IIIII-JJJJJ-KKKKK-LLLLL",1202,"65cc391d-6568-4dcc-a3f1-86a2f04140f5",33333,"CHECKEDOUT",69,22)
	e4 = Node("MMMMM-NNNNN-OOOOO-PPPPP",1203,"65cc391d-6568-4dcc-a3f1-86a2f04140f6",44444,"CHECKEDIN",69,22)
	head = Node(None, 69, None, None, "INITIAL", 0x0E, "Initial block")

	ll = LinkedList()
	ll.head = head
	#ll.append(e2)
	#ll.append(e3)
	#ll.append(e4)
	#ll.verify()
	ll.init()
	ll.print()
    

main()