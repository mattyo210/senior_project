
def scan_write(scanlist):
	username=raw_input("input your user name\n")
	string="".join(map(str, scanlist))+ "\n"
	print(string)
	filename="/home/"+ username +"/catkin_ws/src/robot/nodes/scandata.txt"
	f = open(filename,'w')
   	f.write(string)
	f.close()
	print("fileclose")

if __name__ == "__main__":
    scanlist=[1.23,2.54,3.34,4.34,5.34,6.7777]
    scan_write(scanlist)
