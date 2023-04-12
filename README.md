# salsa
Our info:
    Raul Dayao, 1214758558
    Taran Rich, 1214822466
    Cameron Hartman, 1218967347
    Rachel Guzman, 1219550618

Purpose: The blockchain is to emulate the functionality of a chain of command form.

How it works: To compile the python code and make an executable named bchoc please run "make". When wanting to reset & rerun please run "make clean" followed by the inital step. In summary, we just copy the python code into a binary file then elevate privileges so it can be ran with the arguements.

The blockchain must be initialized before blocks can be added, the add command will initialize the chain if the chain is empty or invalid. Blocks are based on the evidenceID, and so a new block can only be added if there isn't already a block with the same ID. If the blockchain is built correctly and the evidence ID has not been added to the chain, the block is added at the end of the chain with the chain containing the hash of the previous parent block, timestamp of the action, case and evidence ID, and status of CHECKEDIN, since the checked in or out status is used to track the use of a piece of evidence.  

Each of the potential arguements & their flags are encompassed within our arginit() which takes argv(aka user command) as it's parameter to determine what action to carry out. Since the arguements were always at index 1 of argv, this would allow arginit to go through our if conditionals to see if it was a valid arg or not. Within each arguement case, we account for the potential flags that may be thrown within their command, and for possible errors they may cause with invalid commands. Within each arg case we would write to a blockchain file, a log file(useful for the log arg), and an error file(useful for the verify arg).

