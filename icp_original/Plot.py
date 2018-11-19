# -*- coding: UTF-8 -*-
import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

def map_plot(filename):
    fig = plt.figure()
    map=map_make(filename)
    x=map[0]
    y=map[1]
    plt.scatter(y,x,s = 0.4)
    plt.show()

def map_make(filename):
    path = filename
    with open(path) as f:
        # read from text
        s = f.read()
        x = []
        y = []

        s = s.replace("],["," , ")
        s = s.replace("[","")
        s = s.replace("]"," ]")
        sp = s.split()
        count = 0 # there are scan data number of ","

        for i in range(len(sp)):
            if sp[i] == ",":
                if count == 0:
                    first_comma = i # store index of first comma to delte comma
                count = count + 1

        j = 0
        for i in range(count):
            # append until coming comma
            while sp[j] != ",":
                x.append(sp[j])
                j = j + 1
                # append until coming right bracket
            while sp[j] != "]":
                y.append(sp[j])
                j = j + 1
            # remove comma from x
        comma = x[first_comma]
        for i in range(x.count(x[first_comma])):
            x.remove(comma)

        for i in range(len(x)):
            x[i] = float(x[i])
        right = y[0]
        # remove right bracket from y
        for i in range(y.count(y[0])):
            y.remove(right)
        for i in range(len(y)):
            y[i] = float(y[i])

        map=np.array([x,y])
        return map
