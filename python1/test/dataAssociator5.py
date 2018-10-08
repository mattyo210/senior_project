import numpy as np
import re
import math

class DataAssociator():

	def __init__(self):
		self.file_read()


	def file_read(self):
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
		#print(scan[152])
		self.find_correspondence(len(c)-1, scan)


	def find_correspondence(self, scan_len, scan):
		DTHRE = 0.2	
		rlp = []
		glp = []
		global ref_lps
		ref_lps = []
		global cur_lps
		cur_lps = []
		count = 0
		evthre = 0.000001

		for k in range(scan_len):
			evmin = []
			variation = np.inf
			if count ==0:
				rlp = self.globalpoint(scan[k])
				glp = self.globalpoint(scan[k+1])
			elif count > 0:
				glp = self.globalpoint(scan[k+1])

			for i in range(len(glp)): # glp
				dmin = np.inf
				rlpmin = None
				for j in range(len(rlp)): # rlp
					d = (glp[i][0] - rlp[j][0])**2 + (glp[i][1]-rlp[j][1])**2
					if d <= DTHRE**2 and d < dmin:
						dmin = d
						rlpmin = rlp[j]
			
				if rlpmin is not None:
					#print(rlpmin)
					#print(i, glp[i])
					cur_lps.append(glp[i])
					ref_lps.append(rlpmin)

			#print(len(ref_lps))
			#for l in range(len(ref_lps)):
			#	print("find_correspondence", l)
			#	print(cur_lps[l])
			#	print(ref_lps[l])
			#print(cur_lps, ref_lps)
			#quit()

			self.optimize_pose(scan[k+1])

			count+=1
			rlp = glp


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
		evthre = 0.5
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
		return tx, ty, th, evmin
		

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
