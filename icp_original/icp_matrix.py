import numpy as np
import re
import math
import Plot
import time
"display=True"
plot=True
def scan_match():
    all_scan=file_read()
    start = time.time()
    final_map=icp(all_scan)
    end = time.time()
    print(end-start)
    #file_write(rob_pos,"rob_pos.txt")
    file_write(final_map,"mapdata.txt")

    if plot==True:
        Plot.map_plot("mapdata.txt")

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

def file_write(data,file_name):
    f = open(file_name,"w")
    f.write(data)
    f.write("\n")
    f.close()

def icp(scan):
    global ref_glp
    global cur_scan
    global cur_match
    global ref_match
    final_map=""
    e=0.0000001
    rob_pose_x=[]
    rob_pose_y=[]
    for i in range(len(scan)-1):
        icp_error=[10000,1000]
        i_cur_error=100
        print("now..."+str(100*(i+1)/len(scan))+"%")
        if i==0:
            ref_glp=convert_glp(scan[i])
        cur_scan=scan[i+1]
        while (icp_error[1]-icp_error[0])**2>e**2:
            #print("yaa")
            ref_match,cur_match=associate(ref_glp,cur_scan)
            cur_scan,i_cur_error=optimize()
            icp_error.insert(0,i_cur_error)
            #print("icpshuusoku;"+str((icp_error[1]-icp_error[0])**2))
        ref_match,cur_match=associate(ref_glp,cur_scan)
        ref_glp=convert_glp(cur_scan)
        new_map=cur_match
        str_new_map=",".join(map(str, new_map))+ "\n"
        final_map +=str_new_map


    return final_map

def optimize():
    global ref_glp
    global cur_match
    global ref_match
    global cur_scan
    error=[100000,1000]
    cur_error=100
    lr=0.001
    e=0.000001
    x=np.array(cur_scan[:3])
    new_pose=x
    #print("yaa")
    #print("odometry"+str(new_pose))
    while (error[1]-error[0])**2>e**2:
        grad_pose,cur_error=numerical_gradient(loss,x)
        error.insert(0,cur_error)
        #print("grad="+str(grad_pose))
        x-= lr * grad_pose
        #print("cur_error"+str(cur_error))
        #print("syuusoku1:"+str((error[1]-error[0])**2))
    cur_scan[:3]=x
    #print(cur_scan)
    return cur_scan,cur_error

def numerical_gradient(f, x):
    h= 1e-7 # 0.0001
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
        x[idx] = tmp_val
        it.iternext()
    return grad,error


def loss(x):
    global ref_match
    global cur_match
    all_error=0
    old_x=np.array(cur_scan[:3])
    old_t=np.array([[old_x[0]],[old_x[1]]])
    #print(x)
    t=np.array([[x[0]],[x[1]]])
    rad=x[2]-old_x[2]
    R=np.array([[np.cos(rad), -np.sin(rad)],
                [np.sin(rad), np.cos(rad)]])
    opt_cur_match=np.dot(R,cur_match-old_t)+t
    u=(opt_cur_match-ref_match)**2
    error=1/2*(sum(u[0])+sum(u[1]))
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
        if glp_x != inf and glp_y != inf and glp_x != 0.00000 and glp_y != 0.000000:
            x.append(float(glp_x))
            y.append(float(glp_y))
    glp = np.array([x,y])
    return glp

def associate(ref_glp,cur_scan):
    DTHRE = 0.1
    evthre = 0.1
    cur_x = []
    cur_y = []
    ref_x = []
    ref_y = []
    cur_glp=convert_glp(cur_scan)
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
    return ref_match,cur_match

def main():
    scan_match()

if __name__ == "__main__":
	main()
