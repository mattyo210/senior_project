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
			#print(cur_scan)
			self.find_correspondence(rlp, glp)
			rlp = glp
			count += 1
			del evmin_[:]
			varitation=np.inf



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
		print(cur_lps)
		print(ref_lps)

		opt_cur = self.optimize_pose(cur_scan)
		evmin_.append(opt_cur[3])
		#print(evmin_)
		#k += 1
		#print(k)
		if len(evmin_) >= 2:
			variation = evmin_[k-1] - evmin_[k]
			print (varitation)
		#while evthre < variation:
			#for l in range(3):
				#cur_scan[l] = opt_cur[l]
			#glp = self.globalpoint(cur_scan)
			#self.find_correspondence(rlp, glp)

		#kokodefailenikakikomu
		f = open("data.txt","a")
		maped_glp = map(str,cur_lps)
		mojiretsu = ','.join(maped_glp)
		f.write(mojiretsu)
		f.write("\n")
		f.close()

		#print(opt_cur[0],opt_cur[1],opt_cur[2])
		#print(glp)





	def globalpoint(self, glp):
		a = []
		inf = np.inf
		for i in range(3,len(glp)):
			# fildata(odometry(x,y,z)+scan(0..359))
			glp_x = glp[0] + glp[i] * math.cos(math.radians(i-3) + glp[2])
			glp_y = glp[1] + glp[i] * math.sin(math.radians(i-3) + glp[2])


			if math.fabs(glp_x)!= inf and math.fabs(glp_y)!= inf:
				b = np.array([glp_x, glp_y])
				a.append(b)

		data = np.array(a)
		#print(data)
		return data


	def optimize_pose(self, init_pose):
		tx = init_pose[0]
		ty = init_pose[1]
		th = init_pose[2]


		txmin = tx
		tymin = ty
		thmin = th
		x=np.array([tx,ty,th])
		#print(x)
		evmin = np.inf
		evold = evmin
		# cost
		evthre = 0.2
		lr = 0.1

		ev = self.cal_value(x)

		while abs(evold - ev) > evthre:
			evold=ev
			grad=self.numerical_gradient(self.cal_value, x)
			x -= lr *grad
			ev=self.cal_value(x)
			tx=x[0]
			ty=x[1]
			th=x[2]
			if ev < evmin:
				evmin=ev
				txmin=x[0]
				tymin=x[1]
				thmin=x[2]
				#print(txmin,tymin,thmin)
		return txmin, tymin, thmin, evmin

	def numerical_gradient(self,f, x):
		h= 1e-4 # 0.0001
		grad = np.zeros_like(x)

		it = np.nditer(x, flags=['multi_index'], op_flags=['readwrite'])
		while not it.finished:
			idx = it.multi_index
			tmp_val = x[idx]
			x[idx] = float(tmp_val) + h
			fxh1 = f(x) # f(x+h)

			x[idx] = tmp_val - h
			fxh2 = f(x) # f(x-h)
			grad[idx] = (fxh1 - fxh2) / (2*h)

			x[idx] = tmp_val # 値を元に戻す
			it.iternext()

		return grad


	def cal_value(self,x):
		global ref_lps, cur_lps
		evlimit = 0.1
		error = 0
		pn = 0
		nn = 0
		tx=x[0]
		ty=x[1]
		th=x[2]

		for i in range(len(cur_lps)):
			clp = cur_lps[i]
			rlp = ref_lps[i]
			cx = clp[0]
			cy = clp[1]
			x = math.cos(th) * cx - math.sin(th) * cy + tx
			y = math.sin(th) * cx - math.cos(th) * cy + ty
			edis = (x - rlp[0])**2 + (y - rlp[1])**2
			#print(edis)
			if edis <= evlimit**2:
				#print(pn)
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
