import numpy as np
import re
import math

import icp

class DataAssociator():

	def __init__(self):
		global evmin
		global variation
		global k
		evmin_ = []
		variation = np.inf
		k = -1
		self.file_read()


	def file_read(self):
		global old_cur
		global new_clp
		count = 0
		path = 'scandata.txt'
	    	with open(path) as f:
			a = []
			b = []
			c = []
			c = f.read().splitlines()
			#print(len(c))
			for i in range(len(c)):
				b = c[i].split( )
				numbers = []
				for j in b:
					numbers.append(float(j))
				a.append(numbers)
		scan = np.array(a)

		for i in range(len(c)-1):
			if count ==0:
				rlp = self.globalpoint(scan[i])
				clp = self.globalpoint(scan[i+1])

			elif count > 0:
				clp = self.globalpoint(scan[i+1])
			
			#print(rlp)
			#print(rlp[0][0])   # indicate x
			#print(rlp[1][0])   # indicate y
	
			old_cur = scan[i+1]
			self.find_correspondence(rlp, clp)
			rlp = new_clp
			count += 1


	def find_correspondence(self, rlp, clp):
		global variation
		global k
		global new_clp
		DTHRE = 0.2	
		global ref_lps
		ref_lps = []
		global cur_lps
		cur_lps = []
		count = 0
		evthre = 0.000001

		cur_x = []
		cur_y = []
		ref_x = []
		ref_y = []
		global old_cur
		error = []
				
		for i in range(len(clp[0])): # clp count x : len(x)
			dmin = np.inf
			rlpmin_x = None
			rlpmin_y = None
			for j in range(len(rlp[0])): # rlp

				d = (clp[0][i] - rlp[0][j])**2 + (clp[1][i] - rlp[1][j])**2 
				#print("d= "+str(d))

				if d <= DTHRE**2 and d < dmin:
					dmin = d
					rlpmin_x = rlp[0][j]
					rlpmin_y = rlp[1][j]
		
			if rlpmin_x is not None:
				cur_x.append(clp[0][i])
				cur_y.append(clp[1][i])
				ref_x.append(rlpmin_x)
				ref_y.append(rlpmin_y)		
			
		cur_match = np.array([cur_x,cur_y])
		ref_match = np.array([ref_x,ref_y])		

		R, T, error = icp.cal(ref_match,cur_match)
		#print(R)
		#print(T)
		print("error= "+str(error))

		cur_position = np.array([old_cur[0],old_cur[1]])
		cur_position = cur_position.reshape([2,1])

		# new_cur is location in map
		new_cur = R * cur_position + T
		#print(new_cur)
		old_cur[0] = new_cur[0]
		old_cur[1] = new_cur[1]
		old_cur[2] = math.atan2(old_cur[1],old_cur[0])
		clp = self.globalpoint(old_cur)
		new_clp = clp
		self.find_correspondence(rlp, clp)
		quit()


		error.append()
		k += 1
		print(k)
		if len(error) >= 2:
			variation = error[k-1] - error[k]
			while evthre < variation:
				for l in range(3):
					cur_scan[l] = opt_cur[l]
				new_clp = self.globalpoint(cur_scan)
				variation = np.inf
				self.find_correspondence(rlp, new_clp)

		#kokodefailenikakikomu
		f = open("data.txt","a")
		maped_clp = map(str,new_clp)
		mojiretsu = ','.join(maped_clp)
		f.write(mojiretsu)
		f.write("\n")
		f.close()

		print(opt_cur[0],opt_cur[1],opt_cur[2])
		#print(new_clp)
		evmin_ = []
		variation = np.inf
		k = -1


	def globalpoint(self, scan):
		x = []
		y = []
		glp = []
		inf = -np.inf

		for i in range(3,len(scan)):
			# fildata(odometry(x,y,z)+scan(0..359))
			glp_x = scan[0] + scan[i] * math.cos(math.radians(i-3) + scan[2])
			glp_y = scan[1] + scan[i] * math.sin(math.radians(i-3) + scan[2])
			if glp_x != inf and glp_y != inf:
				x.append(float(glp_x))
				y.append(float(glp_y))

		glp = np.array([x,y])

		return glp

def main():
	DataAssociator()	

if __name__ == "__main__":
	main()
