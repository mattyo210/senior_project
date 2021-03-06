"""
Iterative Closest Point (ICP) SLAM example
author: Atsushi Sakai (@Atsushi_twi)
"""

import math
import numpy as np
import matplotlib.pyplot as plt

#  ICP parameters
EPS = 0.0001
MAXITER = 100

ON = True
OFF = False

show_animation = ON


def ICP_matching(ppoints, cpoints):
    """
    Iterative Closest Point matching
    - input
    ppoints: 2D points in the previous frame
    cpoints: 2D points in the current frame
    - output
    R: Rotation matrix
    T: Translation vector
    """
    H = None  # homogeneraous transformation matrix

    dError = 1000.0
    preError = 1000.0
    count = 0

    while dError >= EPS:
        count += 1

        if show_animation:
            plt.cla()
            plt.plot(ppoints[0, :], ppoints[1, :], ".r")
            plt.plot(cpoints[0, :], cpoints[1, :], ".b")
            plt.plot(0.0, 0.0, "xr")
            plt.axis("equal")
            plt.pause(1.0)

        inds, error = nearest_neighbor_assosiation(ppoints, cpoints)
        Rt, Tt = SVD_motion_estimation(ppoints[:, inds], cpoints)

        # update current points
        cpoints = (Rt * cpoints) + Tt

        H = update_homogenerous_matrix(H, Rt, Tt)

        dError = abs(preError - error)
        preError = error
        #print("Residual:", error)

        if dError <= EPS:
            #print("Converge", error, dError, count)
            break
        elif MAXITER <= count:
            #print("Not Converge...", error, dError, count)
            break

    R = np.matrix(H[0:2, 0:2])
    T = np.matrix(H[0:2, 2])

    return R, T, error


def update_homogenerous_matrix(Hin, R, T):

    H = np.matrix(np.zeros((3, 3)))

    H[0, 0] = R[0, 0]
    H[1, 0] = R[1, 0]
    H[0, 1] = R[0, 1]
    H[1, 1] = R[1, 1]
    H[2, 2] = 1.0

    H[0, 2] = T[0, 0]
    H[1, 2] = T[1, 0]

    if Hin is None:
        return H
    else:
        return Hin * H


def nearest_neighbor_assosiation(ppoints, cpoints):

    # calc the sum of residual errors
    dcpoints = ppoints - cpoints
    d = np.linalg.norm(dcpoints, axis=0)
    error = sum(d)

    # calc index with nearest neighbor assosiation
    inds = []
    for i in range(cpoints.shape[1]):
        minid = -1
        mind = float("inf")
        for ii in range(ppoints.shape[1]):
            d = np.linalg.norm(ppoints[:, ii] - cpoints[:, i])

            if mind >= d:
                mind = d
                minid = ii

        inds.append(minid)

    return inds, error


def SVD_motion_estimation(ppoints, cpoints):

    pm = np.matrix(np.mean(ppoints, axis=1))
    cm = np.matrix(np.mean(cpoints, axis=1))

    pshift = np.matrix(ppoints - pm)
    cshift = np.matrix(cpoints - cm)

    W = cshift * pshift.T
    u, s, vh = np.linalg.svd(W)

    R = (u * vh).T
    t = pm - R * cm

    return R, t


def cal(ref, cur):
    #print(__file__ + " start!!")

    ref = np.matrix(ref)
    cur = np.matrix(cur)

    nsim = 1  # number of simulation

    for _ in range(nsim):
	
        R, T, error = ICP_matching(ref, cur)

    return R, T, error


if __name__ == '__main__':
    cal()
