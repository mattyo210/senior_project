import numpy as np
import icp_matrix
ref_match=np.array([[0,1,2,2,2,1,0,0],
                    [0,0,0,1,2,2,2,1]])

x=[0.5,0.5,0.785398]
t=np.array([[x[0]],[x[1]]])
rad=x[2]
rot=np.array([[np.cos(rad), -np.sin(rad)],
                  [np.sin(rad), np.cos(rad)]])
cur_match=np.dot(rot,ref_match)+t


c=[[1,1,1],[0,0,0]]
a=np.array(c)
b=np.array([[2,2,2],[1,1,1]])
d=a-b
f=[1,2,3,4]
rad=3.14
old_x=np.array(f[:3])
old_t=np.array([[old_x[0]],[old_x[1]]])
print(old_t)

rot=np.array([[np.cos(rad), -np.sin(rad)],
                  [np.sin(rad), np.cos(rad)]])
e=b
u=(a-e)**2
print(sum(u[0]))
err=sum(u[0])+sum(u[1])
print(err)
all_error=0
for i in range(len(a)-1):
    error2=(a[0][i]-e[0][i])**2+(a[1][i]-e[1][i])**2
    all_error += error2
print(all_error)
