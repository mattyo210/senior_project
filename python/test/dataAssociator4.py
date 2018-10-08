import numpy as np
import re
import math

class DataAssociator():

	def __init__(self):
		
		path = 'scandata.txt'
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
		for i in range(3,len(glp)):
			# fildata(odometry(x,y,z)+scan(0..359))
			glp_x = glp[0] + glp[i] * math.cos(i-3 + glp[2])
			glp_y = glp[1] + glp[i] * math.sin(i-3 + glp[2])

			b = np.array([glp_x, glp_y])
			a.append(b)

		data = np.array(a)
		return data

	def find_correspondence(self, scan):
		DTHRE = 0.2	
		rlp = []
		glp = []
		global ref_lps
		ref_lps = []
		global cur_lps
		cur_lps = []

		rlp = self.globalpoint(scan[0])
		glp = self.globalpoint(scan[1])

		# print(rlp)
		# print(glp)

		for i in range(len(glp)): # glp
			dmin = np.inf
			#dmin = 1000
			rlpmin = None
			for j in range(len(rlp)): # rlp
				d = (glp[i][0] - rlp[j][0])**2 + (glp[i][1]-rlp[j][1])**2
				#print(d)
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
		#for k in range(len(ref_lps)):
		#	print("find_correspondence", k)
		#	print(cur_lps[k])
		#	print(ref_lps[k])
		# print(cur_lps, ref_lps)

		self.optimize_pose(scan[1])


	def optimize_pose(self, init_pose):
		tx = init_pose[0]
		ty = init_pose[1]
		th = init_pose[2]
		txmin = tx
		tymin = ty
		thmin = th
		evmin = np.inf
		evold = evmin
		# cost
		evthre = 1.0
		dd = 0.1
		da = 0.1

		ev = self.cal_value(tx, ty, th)
		kk = 0.00001
		while abs(evold - ev) > evthre:
			evold = ev

			detx = (self.cal_value(tx + dd, ty, th) - ev) / dd
			dety = (self.cal_value(tx, ty + dd, th) - ev) / dd
			deth = (self.cal_value(tx, ty, th + da) - ev) / dd

			dx = -kk * detx
			dy = -kk * dety
			dth = -kk * deth
			tx += dx
			ty += dy
			th += dth
		
			ev = self.cal_value(tx, ty, th)

			if ev < evmin:
				evmin = ev
				txmin = tx
				tymin = ty
				thmin = th

		print(tx, ty, th)
		

	def cal_value(self, tx, ty, th):
		global ref_lps, cur_lps
		evlimit =0.1
		error = 0
		pn = 0
		nn = 0

		for i in range(len(cur_lps)):
			clp = cur_lps[i]
			rlp = ref_lps[i]

			cx = clp[0]
			cy = clp[1]
			x = math.cos(th) * cx - math.sin(th) * cy + tx
			y = math.sin(th) * cx - math.cos(th) * cy + ty

			edis = (x - rlp[0])**2 + (y - rlp[1])**2

			if edis <= evlimit**2:
				pn+=1
			
			error += edis
			nn+=1
			
		if nn > 0:
			error = error / nn
			if error == 0:
				error = np.inf

		pnrate = 1.0 * pn / nn
		error *= 100
		return(error)

def main():
	DataAssociator()	

if __name__ == "__main__":
	main()
