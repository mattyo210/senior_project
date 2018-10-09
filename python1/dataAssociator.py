import numpy as np
import re
import math
import sys
sys.setrecursionlimit(10000)

class DataAssociator():

	def __init__(self):
		global evmin_
		global variation
		global k
		evmin_ = []
		variation = np.inf
		k = -1
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
			#print(len(c))
			for i in range(len(c)):
				b = c[i].split( )
				numbers = []
				for j in b:
					numbers.append(float(j))
				a.append(numbers)
		scan = np.array(a)
		#print(scan[152])

		for i in range(len(c)-1):
			if count ==0:
				rlp = self.globalpoint(scan[i])
				glp = self.globalpoint(scan[i+1])

				f = open("data.txt","a")
				maped_glp = map(str,rlp)
				mojiretsu = ','.join(maped_glp)
				f.write(mojiretsu)
				f.write("\n")
				f.close()

			elif count > 0:
				glp = self.globalpoint(scan[i+1])
			cur_scan = scan[i+1]
			self.find_correspondence(rlp, glp)
			rlp = glp
			count += 1


	def find_correspondence(self, rlp, glp):
		global evmin_
		global variation
		global k
		global cur_scan
		DTHRE = 0.2	
		global ref_lps
		ref_lps = []
		global cur_lps
		cur_lps = []
		count = 0
		evthre = 0.000001
		
		for i in range(len(glp)): # glp
			dmin = np.inf
			rlpmin = None
			for j in range(len(rlp)): # rlp
				d = (glp[i][0] - rlp[j][0])**2 + (glp[i][1]-rlp[j][1])**2
				if d <= DTHRE**2 and d < dmin:
					dmin = d
					rlpmin = rlp[j]
		
			if rlpmin is not None:
				cur_lps.append(glp[i])
				ref_lps.append(rlpmin)

		opt_cur = self.optimize_pose(cur_scan)
		evmin_.append(opt_cur[3])
		#print(evmin_)
		k += 1
		print(k)
		if len(evmin_) >= 2:
			variation = evmin_[k-1] - evmin_[k]
		while evthre < variation:
			for l in range(3):
				cur_scan[l] = opt_cur[l]
			glp = self.globalpoint(cur_scan)
			self.find_correspondence(rlp, glp)

		#kokodefailenikakikomu
		f = open("data.txt","a")
		maped_glp = map(str,glp)
		mojiretsu = ','.join(maped_glp)
		f.write(mojiretsu)
		f.write("\n")
		f.close()

		print(opt_cur[0],opt_cur[1],opt_cur[2])
		#print(glp)
		evmin_ = []
		variation = np.inf
		k = -1


	def globalpoint(self, glp):
		a = []
		for i in range(3,len(glp)):
			# fildata(odometry(x,y,z)+scan(0..359))
			glp_x = glp[0] + glp[i] * math.cos(math.radians(i-3) + glp[2])
			glp_y = glp[1] + glp[i] * math.sin(math.radians(i-3) + glp[2])

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
		evthre = 0.2
		dd = 0.1
		da = 0.1

		ev = self.cal_value(tx, ty, th)
		kk = 0.00001
		while abs(evold - ev) > evthre:
			evold = ev

			detx = (self.cal_value(tx + dd, ty, th) - ev) / dd
			dety = (self.cal_value(tx, ty + dd, th) - ev) / dd
			deth = (self.cal_value(tx, ty, th + da) - ev) / da

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

		#print(tx, ty, th)
		return tx, ty, th, evmin
		

	def cal_value(self, tx, ty, th):
		global ref_lps, cur_lps
		evlimit = 0.1
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
		else :
			pnrate = 1.0 * pn / nn
			error *= 100
		return(error)

def main():
	DataAssociator()	

if __name__ == "__main__":
	main()
