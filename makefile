all:
	cp blockchain.py bchoc
	chmod +x blockchain.py
	chmod +x bchoc
clean:
	rm -f bchocout
	rm -f logfile.txt
	rm -f bchoc