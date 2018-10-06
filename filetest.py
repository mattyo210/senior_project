
def scan_write(scanlist):
	string="".join(map(str, scanlist))+ "\n"
	print(string)
	f = open('scandata.txt','a')
   	f.write(string)
	f.close()
	print("fileclose")


