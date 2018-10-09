import numpy as np
import re
import math

class DataAssociator():

	def __init__(self):
		self.file_read()

	def file_read(self):
		global cur_scan
		count = 0
		path = 'scandata.txt'
	    	with open(path) as f:
			a = []
			b = []
			c = []
			c = f.read().splitlines()
			for i in range(len(c)):
				b = c[i].split( )
				numbers = []
				for j in b:
					numbers.append(float(j))
				a.append(numbers)
		scan = np.array(a)

		f = open("odometry_map.txt","a")
		for i in range(len(c)-1):
			rlp = self.globalpoint(scan[i])

			maped_glp = map(str,rlp)
			mojiretsu = ','.join(maped_glp)
			f.write(mojiretsu)
			f.write("\n")
			print(i)

		f.close()


	def globalpoint(self, glp):
		a = []
		for i in range(3,len(glp)):
			# fildata(odometry(x,y,z)+scan(0..359))
			glp_x = glp[0] + glp[i] * math.cos(i-3 + math.degrees(glp[2]))
			glp_y = glp[1] + glp[i] * math.sin(i-3 + math.degrees(glp[2]))

			b = np.array([glp_x, glp_y])
			a.append(b)

		data = np.array(a)
		return data

def main():
	DataAssociator()	

if __name__ == "__main__":
	main()
