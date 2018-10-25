import numpy as np
import re
import math

def scan_match():
    all_scan=file_read()
    final_map=icp(all_scan)
    print(final_map)
    file_write(final_map)
    #plot(final_map)

def file_read():
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
    return scan

def file_write(final_map):
    f = open("data.txt","w")
    maped_clp = map(str,final_map)
    mojiretsu = ','.join(maped_clp)
    f.write(mojiretsu)
    f.write("\n")
    f.close()

def icp(scan):
    global ref_glp
    global cur_scan
    final_map=[]
    for i in range(len(scan)-1):
        if i==0:
            ref_glp=convert_glp(scan[i])
        cur_scan=scan[i+1]
        new_map=optimize()

        final_map.append(new_map)
    return final_map

def optimize():
    global ref_glp
    global cur_scan
    error=[np.inf]
    cur_error=0
    lr=0.01
    e=0.01

    while (min(error)-cur_error)**2<e:
        x=cur_scan[:3]
        grad_pose,cur_error=numerical_gradient(loss,x)
        new_pose=lr*grad_pose
        cur_scan[:3]=new_pose

    cur_glp=convert_glp(cur_scan)
    ref_match,cur_match=associate(ref_glp,cur_glp)
    new_map=cur_match
    return new_map

def numerical_gradient(f, x):
    h= 1e-4 # 0.0001
    grad = np.zeros_like(x)
    error=f(x)
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
    return grad,error


def loss(x):
    global ref_glp
    global cur_scan

    cur_scan[:3]=x
    cur_glp=convert_glp(cur_scan)
    ref_match,cur_match=associate(ref_glp,cur_glp)

    for i in range(len(cur_match)-1):
        error=(cur_match[0][i]-ref_match[0][i])**2+(cur_match[1][i]-ref_match[1][i])**2
        all_error+=error
    ave_error=error/len(cur_match)

    return ave_error

def convert_glp(scan):
    x = []
    y = []
    glp = []
    inf = -np.inf

    #print(scan[0],scan[1],scan[2])
    for i in range(3,len(scan)):
		# fildata(odometry(x,y,z)+scan(0..359))
        glp_x = scan[0] + scan[i] * math.cos(math.radians(i-3) + scan[2])
        glp_y = scan[1] + scan[i] * math.sin(math.radians(i-3) + scan[2])
        if glp_x != inf and glp_y != inf:
            x.append(float(glp_x))
            y.append(float(glp_y))
    glp = np.array([x,y])
    return glp

def associate(ref_glp,cur_glp):
    DTHRE = 0.2
    evthre = 0.1
    cur_x = []
    cur_y = []
    ref_x = []
    ref_y = []

    for i in range(len(cur_glp[0])): # clp count x : len(x)
        dmin = np.inf
        rlpmin_x = None
        rlpmin_y = None
        for j in range(len(ref_glp[0])): # rlp

            d = (cur_glp[0][i] - ref_glp[0][j])**2 + (cur_glp[1][i] - ref_glp[1][j])**2
				#print("d= "+str(d))
            if d <= DTHRE**2 and d < dmin:
                dmin = d
                rlpmin_x = ref_glp[0][j]
                rlpmin_y = ref_glp[1][j]

        if rlpmin_x is not None:
            cur_x.append(cur_glp[0][i])
            cur_y.append(cur_glp[1][i])
            ref_x.append(rlpmin_x)
            ref_y.append(rlpmin_y)

    cur_match = np.array([cur_x,cur_y])
    ref_match = np.array([ref_x,ref_y])
    print (cur_match)
    return ref_match,cur_match

def main():
    scan_match()

if __name__ == "__main__":
	main()
