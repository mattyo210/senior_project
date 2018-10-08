import numpy as np
import re
import math

class DataAssociator():

	def __init__(self):
		
		path = 'test2.lsc'
    		with open(path) as f:
			a = []
			b = []
			c = []
			c = f.read().splitlines()
			for i in range(2):
				b = c[i].split( )
				numbers = []
				for j in b:
					numbers.append(float(j))
				#print(numbers)
				a.append(numbers)
		
		scan = np.array(a)
		#print(scan[0])
		#print(scan[1])
		self.find_correspondence(scan)

	def globalpoint(self, glp):
		a = []
		for i in range(3,364):
			# fildata(odometry(x,y,z)+scan(0..359))
			glp_x = glp[0] + glp[i] * math.cos(i-3 + math.degrees(glp[2]))
			glp_y = glp[1] + glp[i] * math.sin(i-3 + math.degrees(glp[2]))

			b = np.array([glp_x, glp_y])
			a.append(b)

		data = np.array(a)
		return data

	def find_correspondence(self, scan):
		DTHRE = 0.2	
		rlp = []
		ref_lps = []
		glp = []	
		cur_lps = []

		rlp = self.globalpoint(scan[0])
		glp = self.globalpoint(scan[1])

		#print(rlp)
		#print("-----------")
		#print(glp)

		for i in range(360): # glp
			dmin = np.inf
			#dmin = 1000
			rlpmin = None
			for j in range(360): # rlp
				d = (glp[i][0] - rlp[j][0])**2 + (glp[i][1]-rlp[j][1])**2
				print(d)
				if d <= DTHRE**2 and d < dmin:
					dmin = d
					rlpmin = rlp[j]
			
			if rlpmin is not None:
				#print(rlpmin)
				#print(i, glp[i])
				cur_lps.append(glp[i])
				ref_lps.append(rlpmin)

		#print(cur_lps)
		#print(ref_lps)

		# ref = glp
		#print(len(ref_lps))
		for k in range(len(ref_lps)):
			print("find_correspondence", k)
			print(cur_lps[k])
			print(ref_lps[k])
		# print(cur_lps, ref_lps)

def main():
	DataAssociator()	

if __name__ == "__main__":
	main()
