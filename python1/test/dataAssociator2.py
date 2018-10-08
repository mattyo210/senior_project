import numpy as np
import re
import math

class DataAssociator():

	def __init__(self):
		global cnt
		cnt = -1
		
		path = 'test2.lsc'
    		with open(path) as f:
			cur_scan = f.read().split()
			numbers = []
			for i in cur_scan:
				numbers.append(float(i))
		print(numbers)
		#print(cur_scan[0])
		#self.find_correspondence(cur_scan)
		self.find_correspondence(numbers)

	def globalpoint(self, glp):
		a = []
		for i in range(3,364):
			glp_x = glp[0] + glp[i] * math.cos(i-3 + glp[2])
			glp_y = glp[1] + glp[i] * math.sin(i-3 + glp[2])

			b = np.array([glp_x, glp_y])
			a.append(b)

		data = np.array(a)
		#print(data)
		return data

	def find_correspondence(self, cur_scan):
		DTHRE = 0.2
		global cnt
		cnt+=1		
		dmin = np.inf
		rlpmin = None
		rlp = []
		glp = []	
		cur_lps = []
		ref_lps = []

		if cnt == 0:
			rlp = self.globalpoint(cur_scan)

		elif cnt > 0:
			glp = self.globalpoint(cur_scan)
			for i in 360:
				for j in 360:
					d = (glp[i][0] - rlp[j][0])**2 + (glp[i][1]-rlp[j][1])**2
					if d <= DTHRE**2 and d < dmin:
						dmin = d
						rlpmin = rlp[j]
						tmp = j
				
				if rlpmin is not None:
					cur_lps.append(clp[i])
					ref_lps.append(rlpmin[tmp])

		ref_lp = cur_lp

		#print(cur_lps, ref_lps)

def main():
	DataAssociator()	

if __name__ == "__main__":
	main()
