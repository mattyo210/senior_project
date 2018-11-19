import numpy as np
import re
import math
import time
import Plot
import icp_matrix
np.set_printoptions(threshold=np.inf)
def map_read():
    mapA=Plot.map_make("mapdata1.txt")
    mapB=Plot.map_make("mapdata2.txt")
    merge_maps=merge(mapA,mapB)
    icp_matrix.file_write(merge_maps,"merge_map.txt")
    Plot.map_plot("merge_map.txt")

def merge(mapA,mapB):
    global cur_match
    global ref_match
    icp_error=[10000,1000]
    i_cur_error=100
    e=0.001
    while (icp_error[1]-icp_error[0])**2>e**2:
        ref_match,cur_match=associate(mapA,mapB)
        new_x,i_cur_error=optimize()
        mapB=fix_map(new_x,mapB)
        icp_error.insert(0,i_cur_error)
    str_mapA=",".join(map(str, mapA))+ "\n"
    str_mapB=",".join(map(str, mapB))+ "\n"
    merge_maps=str_mapA + str_mapB
    return merge_maps

def associate(ref_glp,cur_glp):
    DTHRE = 0.1
    evthre = 0.05
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
    return ref_match,cur_match

def optimize():
    global cur_match
    global ref_match
    error=[100000,1000]
    cur_error=100
    lr=0.00001
    e=0.001
    x=np.array([0.0,0.0,0.0])
    #print("yaa")
    #print("odometry"+str(new_pose))
    while (error[1]-error[0])**2>e**2:
        grad_pose,cur_error=numerical_gradient(loss,x)
        error.insert(0,cur_error)
        print("cur_error:"+ str(cur_error))
        print("syuusoku"+str((error[1]-error[0])**2))
        x-= lr * grad_pose
        cur_match=fix_map(x,cur_match)
    new_x=x
    #print(cur_scan)
    return new_x,cur_error

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
    t=np.array([[x[0]],[x[1]]])
    rad=x[2]
    R=np.array([[np.cos(rad), -np.sin(rad)],
                [np.sin(rad), np.cos(rad)]])
    opt_cur_match=np.dot(R,cur_match)+t
    u=(opt_cur_match-ref_match)**2
    error=1/2*(sum(u[0])+sum(u[1]))
    ave_error=error/len(cur_match)
    return ave_error


def fix_map(x,mapB):
    t=np.array([[x[0]],[x[1]]])
    rad=x[2]
    R=np.array([[np.cos(rad), -np.sin(rad)],
                [np.sin(rad), np.cos(rad)]])
    opt_cur_match=np.dot(R,mapB)+t
    return opt_cur_match

def main():
    map_read()

if __name__ == "__main__":
	main()
